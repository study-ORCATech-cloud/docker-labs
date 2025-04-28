#!/usr/bin/env python3

import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello from Python Flask!',
        'environment': os.environ.get('ENVIRONMENT', 'production'),
        'hostname': os.uname().nodename
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 