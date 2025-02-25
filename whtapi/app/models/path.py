from datetime import datetime, timezone
from bson import ObjectId
from flask import current_app
from app.utils.base62 import objectid_to_base62

def create_path(user_id, path, description=None):
    """Create a new path for a user"""
    db = current_app.db
    
    # Check if path already exists for this user
    if db.paths.find_one({'user_id': user_id, 'path': path}):
        return None, "Path already exists for this user"
    
    path_doc = {
        'user_id': user_id,
        'path': path,
        'description': description,
        'created_at': datetime.now(timezone.utc),
        'last_used': None,
        'webhook_count': 0
    }
    
    # Ensure indexes
    db.paths.create_index([('user_id', 1), ('path', 1)], unique=True)
    db.paths.create_index('user_id')  # For listing paths
    
    result = db.paths.insert_one(path_doc)
    path_doc['_id'] = str(result.inserted_id)
    path_doc['user_id'] = str(user_id)
    
    return path_doc, None

def get_user_paths(user_id):
    """Get all paths for a user"""
    db = current_app.db
    paths = list(db.paths.find({'user_id': user_id}))
    
    # Convert ObjectId to string for JSON serialization
    for path in paths:
        path['_id'] = str(path['_id'])
        path['user_id'] = str(path['user_id'])
        path['base'] = objectid_to_base62(user_id)  # Add base62_id
    
    return paths

def delete_path(user_id, path_id):
    """Delete a path and its associated webhook data"""
    db = current_app.db
    
    try:
        path_obj_id = ObjectId(path_id)
    except:
        return False, "Invalid path ID"
    
    # Find and delete path
    path = db.paths.find_one_and_delete({
        '_id': path_obj_id,
        'user_id': user_id
    })
    
    if not path:
        return False, "Path not found or unauthorized"
    
    # Delete associated webhook data
    db.webhook_data.delete_many({'path_id': path_obj_id})
    
    return True, None

def record_webhook(path_id, user_id, content_type, payload, headers=None, ip_address=None):
    """Record a webhook request"""
    db = current_app.db
    
    # Update path last_used and increment webhook_count
    db.paths.update_one(
        {'_id': path_id},
        {
            '$set': {'last_used': datetime.now(timezone.utc)},
            '$inc': {'webhook_count': 1}
        }
    )
    
    # Store webhook data
    webhook_doc = {
        'path_id': path_id,
        'user_id': user_id,
        'received_at': datetime.now(timezone.utc),
        'content_type': content_type,
        'payload': payload,
        'headers': headers or {},
        'ip_address': ip_address  # Add IP address field
    }
    
    # Ensure indexes
    db.webhook_data.create_index('path_id')
    db.webhook_data.create_index('user_id')
    db.webhook_data.create_index('received_at')
    
    result = db.webhook_data.insert_one(webhook_doc)
    return str(result.inserted_id)

def update_webhook_counts():
    """Update webhook counts for all paths"""
    db = current_app.db
    
    # Get all paths
    paths = db.paths.find({})
    
    for path in paths:
        # Count actual webhooks for this path
        actual_count = db.webhook_data.count_documents({'path_id': path['_id']})
        
        # Update path with actual count
        db.paths.update_one(
            {'_id': path['_id']},
            {'$set': {'webhook_count': actual_count}}
        ) 