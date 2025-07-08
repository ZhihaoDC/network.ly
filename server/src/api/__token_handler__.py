"""
Create the decorator 'token_required' for all Controllers.
"""
from functools import wraps
from flask import jsonify, request
import jwt

from src.services import UserService
from src.models.UserModel import User
from src import app_config        
import sys
       
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()



        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app_config.SECRET_KEY, algorithms=["HS256"])
            user = UserService.get_by_email(User, email=data['sub'])
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError as e:
            print(e, file=sys.stderr)
            return jsonify(expired_msg), 401 
        except (jwt.InvalidTokenError, Exception) as e:
            print(e, file=sys.stderr)
            return jsonify(invalid_msg), 401

    return _verify