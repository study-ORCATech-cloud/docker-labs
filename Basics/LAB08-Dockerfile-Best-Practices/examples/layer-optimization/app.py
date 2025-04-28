#!/usr/bin/env python3

from flask import Flask, jsonify
import os
import redis

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def index():
    # Increment visitor count
    count = redis_client.incr('visitor_count')
    
    return jsonify({
        'message': 'Hello from Flask!',
        'visitor_count': count,
        'hostname': os.uname().nodename
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/data')
def data():
    # This is a placeholder for data access
    return jsonify({'data': 'Sample data from the application'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 