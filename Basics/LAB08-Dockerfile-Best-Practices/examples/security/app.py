#!/usr/bin/env python3

from flask import Flask, request, jsonify
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Mock database for demo purposes
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user': {'password': 'password123', 'role': 'user'}
}

@app.route('/')
def index():
    return jsonify({
        'message': 'Security Example API',
        'version': '1.0.0'
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing credentials'}), 400
    
    username = data['username']
    password = data['password']
    
    # Insecure password check (for demonstration purposes only)
    if username in users and users[username]['password'] == password:
        logger.info(f"User {username} logged in successfully")
        return jsonify({
            'success': True, 
            'role': users[username]['role']
        })
    else:
        logger.warning(f"Failed login attempt for user {username}")
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/data')
def get_data():
    return jsonify({
        'secret_data': 'This is sensitive information'
    })

if __name__ == '__main__':
    # Insecure setup for demonstration
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True) 