from flask import Flask, jsonify, render_template_string
import os
import logging

app = Flask(__name__)

# Configure logging - secure way without exposing secrets
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: These paths define where Docker will mount our secrets
# HINT: The /run/secrets is the conventional path for Docker secrets
# HINT: When using docker-compose, you'll mount your secrets directory here
SECRETS_PATH = '/run/secrets'
DB_PASSWORD_FILE = os.path.join(SECRETS_PATH, 'db_password.txt')
API_KEY_FILE = os.path.join(SECRETS_PATH, 'api_key.txt')
JWT_SECRET_FILE = os.path.join(SECRETS_PATH, 'jwt_secret.txt')

# TODO: This function reads secrets from files mounted by Docker
# HINT: The files must be mounted as a volume in your docker-compose.yml
def read_secret_file(file_path, default=''):
    """Safely read secret from file, with error handling"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            logger.warning(f"Secret file not found: {file_path}")
            return default
    except Exception as e:
        logger.error(f"Error reading secret file {file_path}: {e}")
        return default

# Read secrets from files
db_password = read_secret_file(DB_PASSWORD_FILE, 'db_password_not_found')
api_key = read_secret_file(API_KEY_FILE, 'api_key_not_found')
jwt_secret = read_secret_file(JWT_SECRET_FILE, 'jwt_secret_not_found')

# Secure logging - doesn't expose actual secrets
logger.info("Application starting up - secrets loaded")
logger.info(f"Database password length: {len(db_password)}")
logger.info(f"API key found: {'Yes' if api_key != 'api_key_not_found' else 'No'}")

@app.route('/')
def index():
    """Display information about file-based secrets handling (securely)"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File-Based Secrets Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #28a745;
                border-bottom: 2px solid #28a745;
                padding-bottom: 10px;
            }
            .info {
                background-color: #d1ecf1;
                border: 1px solid #bee5eb;
                color: #0c5460;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .secret-table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            .secret-table th, .secret-table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            .secret-table th {
                background-color: #f2f2f2;
            }
            .source {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 4px;
                font-family: monospace;
            }
            code {
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <h1>File-Based Secrets Management Demo</h1>
        
        <div class="info">
            <strong>Info:</strong> This page demonstrates secure file-based secrets management.
            Secrets are stored in files and mounted into the container.
        </div>
        
        <h2>Secrets Status</h2>
        <table class="secret-table">
            <tr>
                <th>Secret Type</th>
                <th>Source</th>
                <th>Status</th>
                <th>Safe Display</th>
            </tr>
            <tr>
                <td>Database Password</td>
                <td>File Mount</td>
                <td>{{ "Available" if db_password_exists else "Not Found" }}</td>
                <td>{{ db_password_masked }}</td>
            </tr>
            <tr>
                <td>API Key</td>
                <td>File Mount</td>
                <td>{{ "Available" if api_key_exists else "Not Found" }}</td>
                <td>{{ api_key_masked }}</td>
            </tr>
            <tr>
                <td>JWT Secret</td>
                <td>File Mount</td>
                <td>{{ "Available" if jwt_secret_exists else "Not Found" }}</td>
                <td>{{ jwt_secret_masked }}</td>
            </tr>
        </table>
        
        <h2>Security Improvements</h2>
        <ul>
            <li>Secrets stored in separate files with appropriate permissions</li>
            <li>Files mounted as read-only in the container</li>
            <li>Secrets never logged or exposed to the frontend</li>
            <li>App running as non-root user</li>
            <li>Masked displays of sensitive data (first/last few characters only)</li>
            <li>Proper error handling for missing secrets</li>
        </ul>
        
        <h2>Implementation Details</h2>
        <p>Secrets are loaded from the following files:</p>
        <ul>
            <li><code>/run/secrets/db_password.txt</code></li>
            <li><code>/run/secrets/api_key.txt</code></li>
            <li><code>/run/secrets/jwt_secret.txt</code></li>
        </ul>
        
        <div class="source">
            <h3>Example Secret Reading Code</h3>
            <pre>
def read_secret_file(file_path, default=''):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            logger.warning(f"Secret file not found: {file_path}")
            return default
    except Exception as e:
        logger.error(f"Error reading secret file {file_path}: {e}")
        return default
            </pre>
        </div>
        
        <p>Continue to <a href="/api/secure">API endpoint</a> to see secure API responses.</p>
    </body>
    </html>
    """
    
    # Safely mask secrets for display (show first 3 and last 2 chars only)
    def mask_secret(secret, default="Not available"):
        if not secret or secret.endswith('_not_found'):
            return default
        if len(secret) <= 5:
            return "****"
        return f"{secret[:3]}{'*' * (len(secret) - 5)}{secret[-2:]}"
    
    db_password_exists = db_password != 'db_password_not_found'
    api_key_exists = api_key != 'api_key_not_found'
    jwt_secret_exists = jwt_secret != 'jwt_secret_not_found'
    
    # Secure logging that doesn't expose secrets
    logger.info("Rendering index page - displaying secret status")
    
    return render_template_string(
        html_content,
        db_password_exists=db_password_exists,
        api_key_exists=api_key_exists,
        jwt_secret_exists=jwt_secret_exists,
        db_password_masked=mask_secret(db_password),
        api_key_masked=mask_secret(api_key),
        jwt_secret_masked=mask_secret(jwt_secret)
    )

@app.route('/api/secure')
def secure_api():
    """Example of a secure API that doesn't expose secrets"""
    # No sensitive data in response
    data = {
        'status': 'success',
        'message': 'This API response safely uses secrets without exposing them',
        'db_connected': db_password != 'db_password_not_found',
        'api_authenticated': api_key != 'api_key_not_found',
        'environment': os.environ.get('APP_ENV', 'development'),
        # Simulated database query using credentials (without exposing them)
        'data_sample': [
            {'id': 1, 'name': 'Item One'},
            {'id': 2, 'name': 'Item Two'},
            {'id': 3, 'name': 'Item Three'}
        ]
    }
    return jsonify(data)

@app.route('/health')
def health():
    """Health check endpoint"""
    # Check if necessary secrets are available
    secrets_available = (
        db_password != 'db_password_not_found' and
        api_key != 'api_key_not_found'
    )
    
    if secrets_available:
        return jsonify({'status': 'ok', 'secrets_available': True})
    else:
        return jsonify({'status': 'degraded', 'secrets_available': False}), 503

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    # Safer configuration even in development
    app.run(host='0.0.0.0', port=8000, debug=debug_mode) 