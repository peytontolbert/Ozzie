import time
from flask import request, jsonify
from functools import wraps
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class RateLimiter:
    def __init__(self, limit=100, window=60):
        self.limit = limit
        self.window = window
        self.clients = {}
        self.logger = Logger("RateLimiter")
        self.error_handler = ErrorHandler()

    def is_rate_limited(self, client_id):
        current = time.time()
        client_history = self.clients.get(client_id, [])
        
        # Remove old requests
        client_history = [timestamp for timestamp in client_history if current - timestamp < self.window]
        
        if len(client_history) >= self.limit:
            return True
        
        client_history.append(current)
        self.clients[client_id] = client_history
        return False

    def limit(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            client_id = request.remote_addr
            if self.is_rate_limited(client_id):
                self.logger.warning(f"Rate limit exceeded for client: {client_id}")
                return jsonify({'message': 'Rate limit exceeded. Please try again later.'}), 429
            return f(*args, **kwargs)
        return decorated