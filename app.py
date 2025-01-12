# app.py
from datetime import timedelta
from flask import Flask, jsonify, request
import redis
import os

app = Flask(__name__)

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# CREATE: Set a key-value pair in Redis
@app.route('/api/cache', methods=['POST'])
def create_cache():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    if "expire" in data:
        expire = data.get('expire')
        expire = int(expire)
    else:
        expire = 60

    # Client is requesting an unexpirable key/value... log it and do it
    if expire < 0:
        return jsonify({"message": f"Key `{key}` cannot be set with value `{value}` with no expiration."}), 201
    else:
        redis_client.set(key, value, expire)
    return jsonify({"message": f"Key `{key}` set with value `{value}`"}), 201

# READ: Get a value by key from Redis
@app.route('/api/cache/<key>', methods=['GET'])
def get_cache(key):
    value = redis_client.get(key)
    if value:
        ttl = redis_client.ttl(key)
        return jsonify({"key": key, "value": value, "ttl": ttl}), 200
    return jsonify({"message": "Key not found"}), 404

# UPDATE: Update a key-value pair in Redis
@app.route('/api/cache/<key>', methods=['PUT'])
def update_cache(key):
    data = request.json
    new_value = data.get('value')
    if redis_client.exists(key):
        if "expire" in data:
            expire = data.get('expire')
            expire = int(expire)
        else:
            expire = 60

        # Client is requesting an unexpirable key/value... log it and do it
        if expire < 0:
            return jsonify({"message": f"Key `{key}` cannot be set with value `{new_value}` with no expiration."}), 201
        else:
            redis_client.set(key, new_value, expire)
        return jsonify({"message": f"Key `{key}` updated with value `{new_value}`"}), 200
    return jsonify({"message": "Key not found"}), 404

# DELETE: Delete a key from Redis
@app.route('/api/cache/<key>', methods=['DELETE'])
def delete_cache(key):
    if redis_client.exists(key):
        redis_client.delete(key)
        return jsonify({"message": f"Key {key} deleted"}), 200
    return jsonify({"message": "Key not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)