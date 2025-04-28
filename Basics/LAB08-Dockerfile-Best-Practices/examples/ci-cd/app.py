#!/usr/bin/env python3

from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def index():
    hostname = socket.gethostname()
    return jsonify({
        'message': 'Hello from CI/CD Pipeline Demo!',
        'version': os.environ.get('APP_VERSION', '1.0.0'),
        'environment': os.environ.get('ENVIRONMENT', 'production'),
        'hostname': hostname
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 