#!/usr/bin/env python3

from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    # Simulate some processing
    time.sleep(0.1)
    
    return jsonify({
        'message': 'Hello from Flask Caching Example!',
        'version': '1.0.0',
        'hostname': os.uname().nodename
    })

@app.route('/api/data')
def data():
    # This route can be modified to simulate code changes
    return jsonify({
        'data': 'This is sample data',
        'timestamp': time.time()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 