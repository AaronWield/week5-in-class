from functools import wraps
import secrets
from flask import request, jsonify
from flask.json import JSONDecoder, JSONEncoder
from drone_inventory.models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token Missing'}), 401

        try: 
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
        except:
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Invalid token try again'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

import decimal
from flask import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
# Convert any decimal values into strings to allow data to be passed through API call
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
