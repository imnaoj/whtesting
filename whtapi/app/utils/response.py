def api_response(success=True, data=None, error=None):
    response = {
        'success': success,
        'data': data,
        'error': error
    }
    return response 