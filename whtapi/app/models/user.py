from datetime import datetime, timezone
import pyotp
import secrets
from flask import current_app
from app.utils.base62 import objectid_to_base62, base62_to_objectid, is_valid_base62

def generate_secret_key():
    """Generate a random secret key for TOTP"""
    return pyotp.random_base32()

def create_user(email):
    """Create a new user with email and TOTP secret key"""
    db = current_app.db
    
    # Check if user already exists
    if db.users.find_one({'email': email}):
        return None, "Email already registered"
    
    # Generate secret key for TOTP
    secret_key = generate_secret_key()
    
    # Create user document
    user = {
        'email': email,
        'secret_key': secret_key,
        'created_at': datetime.now(timezone.utc),
        'last_login': None
    }
    
    # Insert into database
    db.users.create_index('email', unique=True)
    result = db.users.insert_one(user)
    
    # Add base62_id field based on the generated ObjectId
    base62_id = objectid_to_base62(result.inserted_id)
    
    # Update the document with the base62_id
    db.users.update_one(
        {'_id': result.inserted_id},
        {'$set': {'base62_id': base62_id}}
    )
    
    # Add base62_id to the user dict for the response
    user['base62_id'] = base62_id
    user['_id'] = str(result.inserted_id)

    db.users.create_index('base62_id', unique=True)
    
    return user, None

def verify_totp_codes(email, code1, code2):
    """Verify two consecutive TOTP codes"""
    db = current_app.db
    user = db.users.find_one({'email': email})
    
    if not user:
        return None, "User not found"
    
    if code1 == code2:
        return None, "Codes must be different"
    
    totp = pyotp.TOTP(user['secret_key'])
    window_size = current_app.config['OTP_WINDOW_SIZE']
    
    # Verify both codes are valid within the window
    valid_code1 = totp.verify(code1, valid_window=window_size)
    valid_code2 = totp.verify(code2, valid_window=window_size)
    
    if not (valid_code1 and valid_code2):
        return None, "Invalid codes"
    
    # Update last login using timezone.utc instead of datetime.UTC
    db.users.update_one(
        {'_id': user['_id']},
        {'$set': {'last_login': datetime.now(timezone.utc)}}
    )
    
    return user, None

def get_user_by_base62(base62_id):
    """Find a user by their base62_id
    
    Args:
        base62_id (str): The Base62 ID to look up
        
    Returns:
        tuple: (user_dict, error_message)
            - user_dict: Dictionary containing user data if found, None if not found
            - error_message: Error message if any, None if successful
    """
    db = current_app.db
    
    if not is_valid_base62(base62_id):
        return None, "Invalid Base62 ID format"
    
    try:
        object_id = base62_to_objectid(base62_id)
        user = db.users.find_one({'_id': object_id})
        if user:
            user['_id'] = str(user['_id'])
            return user, None
        return None, "User not found"
    except ValueError as e:
        return None, str(e)

# Example usage in your route:
"""
@auth_bp.route('/user/<base62_id>', methods=['GET'])
def get_user(base62_id):
    user, error = get_user_by_base62(base62_id)
    if error:
        return api_response(False, None, error), 400
    return api_response(True, user)
""" 