#!/usr/bin/env python3
from flask import Flask, jsonify
import datetime
import os
import socket
import platform

app = Flask(__name__)

# Get application version from environment variable
app_version = os.environ.get("APP_VERSION", "1.0.0")

@app.route('/')
def index():
    """Main application route"""
    hostname = socket.gethostname()
    
    return jsonify({
        'app': 'AutoBuild Demo App',
        'version': app_version,
        'hostname': hostname,
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': app_version
    })

@app.route('/info')
def info():
    """Application information endpoint"""
    build_date = os.environ.get("BUILD_DATE", "unknown")
    git_commit = os.environ.get("GIT_COMMIT", "unknown")
    
    return jsonify({
        'name': 'AutoBuild Demo',
        'version': app_version,
        'description': 'Sample application for Docker Hub automated builds',
        'build_date': build_date,
        'git_commit': git_commit,
        'environment': os.environ.get("ENVIRONMENT", "production")
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting AutoBuild Demo App v{app_version} on port {port}")
    app.run(host='0.0.0.0', port=port) 