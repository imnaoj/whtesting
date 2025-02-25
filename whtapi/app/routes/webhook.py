from flask import Blueprint, request, current_app
from bson import ObjectId
from app.models.user import get_user_by_base62
from app.models.path import record_webhook
from app.utils.response import api_response
from datetime import datetime, timezone
from app.utils.websocket import socketio

webhook_bp = Blueprint('webhook', __name__)

def get_client_ip():
    """
    Get the original client IP address using various headers and fallbacks.
    Priority:
    1. X-Real-IP (typically set by nginx)
    2. First IP in X-Forwarded-For (if trusted)
    3. Remote address from request
    """
    # First try X-Real-IP
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip

    # Try X-Forwarded-For
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # Get the first IP in the chain (original client)
        return forwarded_for.split(',')[0].strip()

    # Fallback to remote_addr
    return request.remote_addr

@webhook_bp.route('/<base62_id>/<path:user_path>', methods=['POST'])
def handle_webhook(base62_id, user_path):
    """Handle webhook request for a specific path"""
    # Validate and fetch user
    user, error = get_user_by_base62(base62_id)
    if error:
        return api_response(False, None, error), 404
    
    # Find the path
    path = current_app.db.paths.find_one({
        'user_id': ObjectId(user['_id']),
        'path': user_path
    })
    
    if not path:
        return api_response(False, None, "Path not found"), 404
    
    # Get request data
    content_type = request.headers.get('Content-Type', '')
    
    if 'application/json' in content_type:
        payload = request.get_json(silent=True) or {}
    elif 'application/x-www-form-urlencoded' in content_type:
        payload = request.form.to_dict()
    else:
        payload = request.get_data(as_text=True)

    # Get the client's IP address
    client_ip = get_client_ip()
    
    # Prepare webhook update data
    update_data = {
        'path_id': path['_id'],
        'user_id': ObjectId(user['_id']),
        'received_at': datetime.now(timezone.utc),
        'content_type': content_type,
        'payload': payload,
        'ip_address': client_ip
    }

    # Store the webhook data
    current_app.db.webhook_data.insert_one({
        '_id': ObjectId(), # Generate ID for the webhook
        **update_data
    })
    
    # Update path's webhook count and last_used timestamp
    current_app.db.paths.update_one(
        {'_id': path['_id']},
        {
            '$inc': {'webhook_count': 1},
            '$set': {'last_used': datetime.now(timezone.utc)}
        }
    )

    # Log the emission attempt
    current_app.logger.info(f"Emitting webhook_update to user {user['email']}")
    current_app.logger.info(f"Event data: {update_data}")

    update_data['path_id'] = str(update_data['path_id'])
    update_data['user_id'] = str(update_data['user_id'])
    update_data['received_at'] = update_data['received_at'].isoformat()

    # Emit using socketio directly
    socketio.emit(
        'webhook_update',
        update_data,
        room=user['email'],
        namespace='/'
    )
    
    return api_response(True, update_data) 