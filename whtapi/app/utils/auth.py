from datetime import datetime, timedelta
import jwt
from flask import current_app
from functools import wraps
from flask import request
from app.utils.response import api_response

def generate_token(email):
    """Generate a JWT token for the user"""
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(
            seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        ),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    
    return token 

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return api_response(False, None, "No authorization token"), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decode token
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            
            # Get user
            user = current_app.db.users.find_one({'email': payload['email']})
            if not user:
                raise ValueError("User not found")
            
            # Convert ObjectId to string
            user['_id'] = str(user['_id'])
            
            # Pass user to route
            return f(current_user=user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return api_response(False, None, "Token has expired"), 401
        except (jwt.InvalidTokenError, ValueError) as e:
            return api_response(False, None, str(e)), 401
            
    return decorated 