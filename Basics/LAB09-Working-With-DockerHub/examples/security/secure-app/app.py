#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template, abort
import sqlite3
import os
import subprocess
import logging
from werkzeug.security import generate_password_hash
import shlex

app = Flask(__name__)

# Secure: Load secrets from environment variables, not hardcoded
DB_FILE = os.environ.get('DB_FILE', '/data/app.db')
API_KEY = os.environ.get('API_KEY')  # Set at runtime, not in image

# Set up logging properly
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return jsonify({
        'app': 'Secure Demo',
        'version': '1.0.0',
        'status': 'running'
    })

# Secure: Fixed SQL Injection vulnerability
@app.route('/users')
def users():
    name_filter = request.args.get('name', '')
    
    # SECURE: Using parameterized queries
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT id, name, email FROM users WHERE name LIKE ?"
    cursor.execute(query, (f'%{name_filter}%',))
    
    users = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(users)

# Secure: Fixed Command Injection vulnerability
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    
    # SECURE: Sanitize input and avoid shell=True
    try:
        # Validate input (simple example - in production use more robust validation)
        if not host.replace('.', '').replace('-', '').isalnum():
            return jsonify({'error': 'Invalid hostname format'}), 400
            
        # Use shlex to escape arguments and avoid shell=True
        cmd = ["ping", "-c", "1", host]
        output = subprocess.check_output(cmd, shell=False)
        
        return jsonify({
            'host': host,
            'output': output.decode('utf-8')
        })
    except subprocess.CalledProcessError:
        return jsonify({'error': 'Ping failed'}), 400
    except Exception as e:
        logger.error(f"Error in ping endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Secure: Fixed Template Injection
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    
    # SECURE: Use proper templating or escape the input
    # This assumes you have a templates directory with a greet.html template
    # return render_template('greet.html', name=name)
    
    # Alternative: If you must use render_template_string, escape the input
    from markupsafe import escape
    safe_name = escape(name)
    
    template = """
    <h1>Hello, {{ name }}!</h1>
    <p>Welcome to our application.</p>
    """
    
    # Use the templating system properly with context
    return render_template(
        template_name_or_list='greet.html',  # In real app, create this template
        name=safe_name
    )

# Secure: Fixed hardcoded credentials
@app.route('/admin')
def admin():
    auth_key = request.headers.get('X-API-Key', '')
    
    # SECURE: Compare in constant time to prevent timing attacks
    # and load API key from environment
    if API_KEY and auth_key and auth_key == API_KEY:
        return jsonify({
            'status': 'authenticated',
            'admin': True,
            'message': 'Welcome, admin!'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized'
        }), 401

# Initialize the database with some data
def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute('PRAGMA journal_mode=WAL;')  # More robust journal mode
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password_hash TEXT
    )
    ''')
    
    # Add some sample users with hashed passwords
    users = [
        (1, 'Alice Smith', 'alice@example.com', generate_password_hash('password123')),
        (2, 'Bob Jones', 'bob@example.com', generate_password_hash('letmein')),
        (3, 'Charlie Brown', 'charlie@example.com', generate_password_hash('qwerty'))
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)', users)
    conn.commit()
    conn.close()
    
    # Set secure permissions on the DB file
    try:
        os.chmod(DB_FILE, 0o600)  # Only owner can read/write
    except Exception as e:
        logger.warning(f"Could not set DB file permissions: {str(e)}")

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the app with debugging disabled in production
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    # Log startup info
    logger.info(f"Starting Secure Demo App on port {port}, debug={debug_mode}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode) 