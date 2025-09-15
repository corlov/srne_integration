from functools import wraps
from flask import request, jsonify, g
import common.utils as u


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(message='Missing authorization'), 401
        
        error, token_data = u.check_auth(auth_header)
        if error:
            return error

        g.token_data = token_data
            
        return f(*args, **kwargs)
    return decorated_function