from flask import Flask, jsonify, render_template_string
import os
import logging
import sys

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if get_secret is available (provided by the secrets_manager import hook)
if not hasattr(sys.modules['builtins'], 'get_secret'):
    logger.error("Function get_secret not available - was the app run through secrets_manager.py?")
    
    # For development/fallback only
    def get_secret(name, default=''):
        logger.warning(f"Using fallback get_secret function (not secure) for {name}")
        return default
else:
    # get_secret is injected by secrets_manager.py
    from builtins import get_secret

# Initialize variables
db_password = None
api_key = None
jwt_secret = None

# Load secrets when app starts up
with app.app_context():
    def load_secrets():
        global db_password, api_key, jwt_secret
        
        logger.info("Loading secrets on demand")
        
        # Get secrets using the get_secret function
        db_password = get_secret("db_password", "db_password_not_found")
        api_key = get_secret("api_key", "api_key_not_found")
        jwt_secret = get_secret("jwt_secret", "jwt_secret_not_found")
        
        logger.info(f"Secrets loaded: DB Password: {'Found' if db_password != 'db_password_not_found' else 'Not Found'}")
        logger.info(f"API Key: {'Found' if api_key != 'api_key_not_found' else 'Not Found'}")

@app.route('/')
def index():
    """Display information about the custom secrets management"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Custom Secrets Manager Demo</title>
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
                white-space: pre;
                overflow-x: auto;
            }
            code {
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: monospace;
            }
            .feature {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .feature h3 {
                margin-top: 0;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Custom Secrets Management Demo</h1>
        
        <div class="info">
            <strong>Info:</strong> This page demonstrates a custom secrets management solution for Docker Compose
            that doesn't require Swarm mode.
        </div>
        
        <h2>Secrets Status</h2>
        <table class="secret-table">
            <tr>
                <th>Secret Type</th>
                <th>Status</th>
                <th>Safe Display</th>
            </tr>
            <tr>
                <td>Database Password</td>
                <td>{{ "Available" if db_password_exists else "Not Found" }}</td>
                <td>{{ db_password_masked }}</td>
            </tr>
            <tr>
                <td>API Key</td>
                <td>{{ "Available" if api_key_exists else "Not Found" }}</td>
                <td>{{ api_key_masked }}</td>
            </tr>
            <tr>
                <td>JWT Secret</td>
                <td>{{ "Available" if jwt_secret_exists else "Not Found" }}</td>
                <td>{{ jwt_secret_masked }}</td>
            </tr>
        </table>
        
        <h2>Key Features</h2>
        
        <div class="feature">
            <h3>Encrypted Storage</h3>
            <p>Secrets are stored in encrypted files that can only be decrypted with the correct key.</p>
            <ul>
                <li>AES-256 encryption for all secrets</li>
                <li>Key derivation with PBKDF2</li>
                <li>Separate files for each secret</li>
                <li>Proper file permissions (600)</li>
            </ul>
        </div>
        
        <div class="feature">
            <h3>Memory-Only Access</h3>
            <p>Secrets are only decrypted and stored in memory when needed, never in environment variables.</p>
            <ul>
                <li>Avoids exposure in process lists</li>
                <li>Prevents leakage through docker inspect</li>
                <li>Application accesses secrets via get_secret() function</li>
                <li>No secret values in logs or stack traces</li>
            </ul>
        </div>
        
        <div class="feature">
            <h3>Secrets Management</h3>
            <p>A full CLI interface for creating, listing, and using secrets:</p>
            <div class="source">
# Create a new secret
python secrets_manager.py create db_password

# List available secrets
python secrets_manager.py list

# Run application with secrets available
python secrets_manager.py run app.py
            </div>
        </div>
        
        <h2>How to Use in Your Application</h2>
        <p>Import and use the get_secret function to safely retrieve secrets:</p>
        <div class="source">
# When run through secrets_manager.py, this function is available
db_password = get_secret("db_password", "default_if_not_found")
api_key = get_secret("api_key")

# Use the secrets in your code
db_connection = create_connection(
    user="admin", 
    password=db_password
)
        </div>
        
        <p>Continue to <a href="/api/data">API endpoint</a> to see secure API usage.</p>
    </body>
    </html>
    """
    
    # Load secrets if not already loaded
    if db_password is None:
        load_secrets()
    
    # Safely mask secrets for display (show first 2 and last 2 chars only)
    def mask_secret(secret, default="Not available"):
        if not secret or secret.endswith('_not_found'):
            return default
        if len(secret) <= 5:
            return "****"
        return f"{secret[:2]}{'*' * (len(secret) - 4)}{secret[-2:]}"
    
    db_password_exists = db_password != 'db_password_not_found'
    api_key_exists = api_key != 'api_key_not_found'
    jwt_secret_exists = jwt_secret != 'jwt_secret_not_found'
    
    # Secure logging that doesn't expose secrets
    logger.info("Rendering index page - custom secrets manager demo")
    
    return render_template_string(
        html_content,
        db_password_exists=db_password_exists,
        api_key_exists=api_key_exists,
        jwt_secret_exists=jwt_secret_exists,
        db_password_masked=mask_secret(db_password),
        api_key_masked=mask_secret(api_key),
        jwt_secret_masked=mask_secret(jwt_secret)
    )

@app.route('/api/data')
def api_data():
    """Example of a secure API that doesn't expose secrets"""
    # Load secrets if not already loaded
    if db_password is None:
        load_secrets()
        
    data = {
        'status': 'success',
        'message': 'Using custom secrets management',
        'credentials_available': {
            'db_password': db_password != 'db_password_not_found',
            'api_key': api_key != 'api_key_not_found',
            'jwt_secret': jwt_secret != 'jwt_secret_not_found',
        },
        'environment': os.environ.get('APP_ENV', 'development'),
        'run_mode': 'Using secrets_manager' if hasattr(sys.modules['builtins'], 'get_secret') else 'Direct execution (not secure)'
    }
    return jsonify(data)

@app.route('/health')
def health():
    """Health check endpoint"""
    # Load secrets if not already loaded
    if db_password is None:
        load_secrets()
        
    secrets_available = (
        db_password != 'db_password_not_found' and
        api_key != 'api_key_not_found'
    )
    
    if secrets_available:
        return jsonify({'status': 'ok', 'secrets_available': True})
    else:
        return jsonify({'status': 'degraded', 'secrets_available': False}), 503

if __name__ == '__main__':
    # Run with secure settings
    app.run(host='0.0.0.0', port=8000, debug=False) 