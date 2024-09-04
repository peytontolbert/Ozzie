import jwt
from functools import wraps
from flask import request, jsonify
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class Authentication:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.logger = Logger("Authentication")
        self.error_handler = ErrorHandler()

    def generate_token(self, user_id):
        try:
            token = jwt.encode({'user_id': user_id}, self.secret_key, algorithm='HS256')
            return token
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating token")
            return None

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                user_id = self.verify_token(token)
                if isinstance(user_id, str):  # Error message
                    return jsonify({'message': user_id}), 401
            except:
                return jsonify({'message': 'Token is invalid!'}), 401
            return f(user_id, *args, **kwargs)
        return decorated