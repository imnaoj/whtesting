from flask import Blueprint, request, current_app
from app.models.user import create_user, verify_totp_codes
from app.utils.response import api_response
from app.utils.auth import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or 'email' not in data:
        return api_response(False, None, "Email is required"), 400
    
    email = data['email'].lower().strip()
    
    # Create new user
    user, error = create_user(email)
    if error:
        return api_response(False, None, error), 400
    
    # Return the secret key for QR code generation
    return api_response(True, {
        'email': user['email'],
        'secret_key': user['secret_key'],
        'base62_id': user['base62_id'],
        'created_at': user['created_at'],
        'last_login': user['last_login']
    })

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'code1', 'code2']):
        return api_response(False, None, "Email and two codes are required"), 400
    
    email = data['email'].lower().strip()
    code1 = data['code1'].strip()
    code2 = data['code2'].strip()
    
    # Verify TOTP codes
    user, error = verify_totp_codes(email, code1, code2)
    if error:
        return api_response(False, None, error), 401
    
    # Generate JWT token
    token = generate_token(user['email'])
    
    return api_response(True, {
        'email': user['email'],
        'token': token
    }) 