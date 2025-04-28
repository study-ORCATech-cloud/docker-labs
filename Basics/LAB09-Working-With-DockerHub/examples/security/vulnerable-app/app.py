#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
import subprocess
import logging

app = Flask(__name__)

# Insecure: Setup a database without proper permissions
DB_FILE = "app.db"
API_KEY = "super-secret-api-key-1234"  # Hardcoded secret

# Insecure: Using a vulnerable dependency version in requirements.txt

@app.route('/')
def index():
    return jsonify({
        'app': 'Vulnerable Demo',
        'version': '1.0.0',
        'status': 'running'
    })

# Insecure: SQL Injection vulnerability
@app.route('/users')
def users():
    name_filter = request.args.get('name', '')
    
    # VULNERABLE: Direct string concatenation in SQL query
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = f"SELECT id, name, email FROM users WHERE name LIKE '%{name_filter}%'"
    cursor.execute(query)
    
    users = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(users)

# Insecure: Command Injection vulnerability
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    
    # VULNERABLE: Unsanitized command execution
    cmd = f"ping -c 1 {host}"
    output = subprocess.check_output(cmd, shell=True)
    
    return jsonify({
        'host': host,
        'output': output.decode('utf-8')
    })

# Insecure: Template Injection
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    
    # VULNERABLE: Template injection
    template = f"""
    <h1>Hello, {name}!</h1>
    <p>Welcome to our application.</p>
    """
    
    return render_template_string(template)

# Insecure: Hardcoded credentials
@app.route('/admin')
def admin():
    auth_key = request.args.get('key', '')
    
    # VULNERABLE: Hardcoded API key check
    if auth_key == API_KEY:
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
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT
    )
    ''')
    
    # Add some sample users
    users = [
        (1, 'Alice Smith', 'alice@example.com', 'password123'),
        (2, 'Bob Jones', 'bob@example.com', 'letmein'),
        (3, 'Charlie Brown', 'charlie@example.com', 'qwerty')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)', users)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the app with debugging enabled (security risk in production)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 