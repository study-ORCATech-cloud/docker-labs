#!/usr/bin/env python3
import os
import socket
import platform
import datetime
from flask import Flask, jsonify

app = Flask(__name__)

# Get environment variables with defaults
app_version = os.environ.get('APP_VERSION', '1.0.0')
app_env = os.environ.get('APP_ENV', 'production')

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'version': app_version,
        'environment': app_env
    })

@app.route('/version')
def version():
    version = app_version
    return jsonify({
        'version': version,
        'major': version.split('.')[0] if '.' in version else version,
        'minor': version.split('.')[1] if '.' in version and len(version.split('.')) > 1 else '0',
        'patch': version.split('.')[2] if '.' in version and len(version.split('.')) > 2 else '0',
        'environment': app_env
    })

@app.route('/info')
def info():
    hostname = socket.gethostname()
    try:
        ip_addr = socket.gethostbyname(hostname)
    except:
        ip_addr = '127.0.0.1'
        
    return jsonify({
        'app': 'tagging-demo',
        'version': app_version,
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'environment': app_env,
        'hostname': hostname,
        'ip_address': ip_addr,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting tagging-demo app v{app_version} in {app_env} environment")
    app.run(host='0.0.0.0', port=port, debug=app_env != 'production') 