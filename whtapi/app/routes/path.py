from flask import Blueprint, request, current_app
from bson import ObjectId
from app.utils.response import api_response
from app.utils.auth import require_auth
from app.models.path import (
    create_path,
    get_user_paths,
    delete_path,
    objectid_to_base62
)
from datetime import datetime, timezone, timedelta
from pymongo import DESCENDING

path_bp = Blueprint('path', __name__)

@path_bp.route('/', methods=['GET'])
@require_auth
def list_paths(current_user):
    """List all paths for the authenticated user"""
    paths = get_user_paths(ObjectId(current_user['_id']))
    return api_response(True, paths)

@path_bp.route('/', methods=['POST'])
@require_auth
def add_path(current_user):
    """Create a new path"""
    data = request.get_json()
    
    if not data or 'path' not in data:
        return api_response(False, None, "Path is required"), 400
    
    path = data['path'].strip()
    description = data.get('description')
    
    if not path:
        return api_response(False, None, "Path cannot be empty"), 400
    
    path_doc, error = create_path(
        ObjectId(current_user['_id']),
        path,
        description
    )
    
    if error:
        return api_response(False, None, error), 400
    
    return api_response(True, path_doc), 201

@path_bp.route('/<path_id>', methods=['DELETE'])
@require_auth
def remove_path(current_user, path_id):
    """Delete a path and its webhook data"""
    success, error = delete_path(ObjectId(current_user['_id']), path_id)
    
    if not success:
        return api_response(False, None, error), 404
    
    return api_response(True, None)

@path_bp.route('/<path_id>/data/', methods=['GET'])
@require_auth
def get_path_data(current_user, path_id):
    """Get webhook data for a specific path"""
    try:
        path_obj_id = ObjectId(path_id)
    except:
        return api_response(False, None, "Invalid path ID"), 400

    # Verify path belongs to user
    path = current_app.db.paths.find_one({
        '_id': path_obj_id,
        'user_id': ObjectId(current_user['_id'])
    })
    
    if not path:
        return api_response(False, None, "Path not found or unauthorized"), 404

    # Add base62_id to path data
    path['base'] = objectid_to_base62(ObjectId(current_user['_id']))

    # Get query parameters
    limit = min(int(request.args.get('limit', 10)), 100)  # Max 100 records
    skip = int(request.args.get('skip', 0))
    
    # Get data count
    total_count = current_app.db.webhook_data.count_documents({
        'path_id': path_obj_id
    })

    # Get webhook data
    data = list(current_app.db.webhook_data.find(
        {'path_id': path_obj_id}
    ).sort(
        'received_at', DESCENDING
    ).skip(skip).limit(limit))

    # Convert ObjectIds to strings for JSON serialization
    for item in data:
        item['_id'] = str(item['_id'])
        item['path_id'] = str(item['path_id'])
        item['user_id'] = str(item['user_id'])
        if isinstance(item['received_at'], datetime):
            item['received_at'] = item['received_at'].isoformat()

    response_data = {
        'path': path['path'],
        'total_count': total_count,
        'limit': limit,
        'skip': skip,
        'data': data
    }

    return api_response(True, response_data)

@path_bp.route('/<path_id>/chart/', methods=['GET'])
@require_auth
def get_path_chart_data(current_user, path_id):
    """Get webhook data for charts with 1-minute intervals for last 8 hours"""
    try:
        path_obj_id = ObjectId(path_id)
    except:
        return api_response(False, None, "Invalid path ID"), 400

    # Verify path belongs to user
    path = current_app.db.paths.find_one({
        '_id': path_obj_id,
        'user_id': ObjectId(current_user['_id'])
    })
    
    if not path:
        return api_response(False, None, "Path not found or unauthorized"), 404

    # Get data for last 8 hours (480 minutes)
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(minutes=480)
    
    # Aggregate webhook counts by minute
    pipeline = [
        {
            '$match': {
                'path_id': path_obj_id,
                'received_at': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'year': {'$year': '$received_at'},
                    'month': {'$month': '$received_at'},
                    'day': {'$dayOfMonth': '$received_at'},
                    'hour': {'$hour': '$received_at'},
                    'minute': {'$minute': '$received_at'}
                },
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ]
    
    results = list(current_app.db.webhook_data.aggregate(pipeline))
    
    # Fill in missing minutes with zero counts
    timestamps = []
    counts = []
    current_time = start_date.replace(second=0, microsecond=0)
    
    while current_time <= end_date:
        # Create a matching _id structure for comparison
        current_id = {
            'year': current_time.year,
            'month': current_time.month,
            'day': current_time.day,
            'hour': current_time.hour,
            'minute': current_time.minute
        }
        
        # Find matching count or use 0
        count = next((r['count'] for r in results if r['_id'] == current_id), 0)
        
        timestamps.append(current_time.timestamp() * 1000)  # Convert to milliseconds for JS
        counts.append(count)
        
        # Increment by 1 minute
        current_time += timedelta(minutes=1)

    return api_response(True, {
        'timestamps': timestamps,
        'counts': counts
    }) 