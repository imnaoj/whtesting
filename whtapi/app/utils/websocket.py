from flask_socketio import SocketIO, emit, join_room, leave_room
import jwt
from functools import wraps
from flask import current_app
import logging

logger = logging.getLogger(__name__)

# Initialize with basic config, actual CORS will be set during init_app
socketio = SocketIO(
    logger=True,
    engineio_logger=True,
    path='/ws/socket.io',
    async_mode='gevent'
)

def configure_socketio(app):
    """Configure SocketIO with app's CORS settings"""
    cors_origins = app.config['CORS_ORIGINS']
    
    # If CORS_ORIGINS is a string, convert it to list
    if isinstance(cors_origins, str):
        cors_origins = [origin.strip() for origin in cors_origins.split(',')]
    
    # Update SocketIO CORS settings
    socketio.init_app(
        app,
        cors_allowed_origins=cors_origins,
        path='/ws/socket.io',
        async_mode='gevent'
    )

@socketio.on('connect')
def handle_connect():
    logger.info("Client attempting to connect")
    return True

@socketio.on('authenticate')
def handle_authenticate(token):  # Simplified authentication handler
    logger.info("Authentication attempt received")
    try:
        # Verify token
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        user_email = payload['email']
        logger.info(f"Socket authenticated for user: {user_email}")
        
        # Join user's room
        join_room(user_email)
        
        # Emit success
        emit('authenticated', {
            'status': 'success',
            'email': user_email
        })
        return True
    except Exception as e:
        logger.error(f"Socket authentication failed: {str(e)}")
        emit('authenticated', {
            'status': 'error',
            'message': 'Authentication failed'
        })
        return False

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected")

def emit_webhook_update(user_email, data):
    """Emit webhook update to specific user"""
    logger.info(f"Emitting webhook update to user: {user_email}")
    logger.debug(f"Webhook data: {data}")
    socketio.emit('webhook_update', data, room=user_email) 