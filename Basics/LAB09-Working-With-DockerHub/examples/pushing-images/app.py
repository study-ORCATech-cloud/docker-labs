#!/usr/bin/env python3

from flask import Flask, jsonify
import os
import socket
import datetime

# Create Flask app
app = Flask(__name__)

# Get hostname
hostname = socket.gethostname()

# Get version from environment variable or default
version = os.environ.get("APP_VERSION", "1.0.0")

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello from Docker Hub Demo App!',
        'version': version,
        'hostname': hostname,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': version
    })

@app.route('/info')
def info():
    return jsonify({
        'app_name': 'Docker Hub Demo',
        'version': version,
        'python_version': os.environ.get("PYTHON_VERSION", "unknown"),
        'environment': os.environ.get("ENVIRONMENT", "production"),
        'hostname': hostname,
        'ip_address': socket.gethostbyname(hostname)
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 8080
    port = int(os.environ.get("PORT", 8080))
    
    # Print startup message
    print(f"Starting Docker Hub Demo App v{version} on port {port}")
    
    # Run the app
    app.run(host='0.0.0.0', port=port) 