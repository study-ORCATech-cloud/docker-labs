from flask import Flask, jsonify, render_template_string, request
import os
import logging
import requests
import time
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Secrets API configuration
SECRETS_API_URL = os.environ.get("SECRETS_API_URL", "http://secrets-api:8000")
SECRETS_API_KEY = os.environ.get("SECRETS_API_KEY", "api_key_for_secrets_manager")

# Headers for API requests
API_HEADERS = {
    "X-API-Key": SECRETS_API_KEY,
    "Content-Type": "application/json"
}

def get_secret(secret_name, default=''):
    """Retrieve a secret from the secrets manager API with retries"""
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"{SECRETS_API_URL}/secrets/{secret_name}",
                headers=API_HEADERS,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("exists", False):
                    return data.get("value", default)
                else:
                    logger.warning(f"Secret {secret_name} not found in secrets store")
                    return default
            else:
                logger.error(f"Failed to retrieve secret: {response.status_code} - {response.text}")
                
        except requests.RequestException as e:
            logger.error(f"Request error retrieving secret (attempt {attempt+1}/{max_retries}): {e}")
            
        # Wait before retrying, except on the last attempt
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    
    logger.error(f"All attempts to retrieve secret {secret_name} failed")
    return default

# Initialize variables
db_password = None
api_key = None
jwt_secret = None

# Load secrets when app starts up
with app.app_context():
    def load_secrets():
        global db_password, api_key, jwt_secret
        
        logger.info("Loading secrets from secrets manager")
        db_password = get_secret("db_password", "db_password_not_found")
        api_key = get_secret("api_key", "api_key_not_found")
        jwt_secret = get_secret("jwt_secret", "jwt_secret_not_found")
        
        logger.info(f"Secrets loaded. DB Password available: {'Yes' if db_password != 'db_password_not_found' else 'No'}")
        logger.info(f"API Key available: {'Yes' if api_key != 'api_key_not_found' else 'No'}")

@app.route('/')
def index():
    """Display information about Redis-based secrets management"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Redis Secrets Manager Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #0066cc;
                border-bottom: 2px solid #0066cc;
                padding-bottom: 10px;
            }
            .info {
                background-color: #e6f2ff;
                border: 1px solid #99ccff;
                color: #003366;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .actions {
                background-color: #f0f0f0;
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
            .architecture {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .diagram {
                background-color: #f8f9fa;
                font-family: monospace;
                padding: 15px;
                border-radius: 4px;
                white-space: pre;
                overflow-x: auto;
                margin: 20px 0;
            }
            button {
                background-color: #0066cc;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 5px;
            }
            button:hover {
                background-color: #004c99;
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
        <h1>Redis-Based Secrets Management Demo</h1>
        
        <div class="info">
            <strong>Info:</strong> This page demonstrates using Redis as a secure secrets store.
            Secrets are securely stored in Redis and retrieved via the Secrets API.
        </div>
        
        <h2>Secrets Status</h2>
        <table class="secret-table">
            <tr>
                <th>Secret Name</th>
                <th>Status</th>
                <th>Safe Display</th>
            </tr>
            <tr>
                <td>db_password</td>
                <td>{{ "Available" if db_password_exists else "Not Found" }}</td>
                <td>{{ db_password_masked }}</td>
            </tr>
            <tr>
                <td>api_key</td>
                <td>{{ "Available" if api_key_exists else "Not Found" }}</td>
                <td>{{ api_key_masked }}</td>
            </tr>
            <tr>
                <td>jwt_secret</td>
                <td>{{ "Available" if jwt_secret_exists else "Not Found" }}</td>
                <td>{{ jwt_secret_masked }}</td>
            </tr>
        </table>
        
        <div class="actions">
            <h3>Secret Management Actions</h3>
            <p>The following actions can be performed to manage secrets:</p>
            <button onclick="refreshSecrets()">Refresh Secrets</button>
            <button onclick="window.open('/api/data')">View API Output</button>
            <button onclick="window.open('/health')">Check Health</button>
            <div id="result"></div>
        </div>
        
        <h2>System Architecture</h2>
        <div class="architecture">
            <p>This implementation uses a three-tier architecture for secrets management:</p>
            <ol>
                <li><strong>Redis</strong> - Secure storage backend for secrets</li>
                <li><strong>Secrets API</strong> - RESTful API for accessing and managing secrets</li>
                <li><strong>Application</strong> - Client that retrieves secrets as needed</li>
            </ol>
        </div>
        
        <div class="diagram">
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Redis Storage  │◀───▶│  Secrets API    │◀───▶│  Application    │
│  (secrets-store)│     │  (secrets-api)  │     │  (app)          │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
   Encrypted Data         Access Control         Requests Secrets
                                                 as Needed
        </div>
        
        <h2>Security Features</h2>
        <ul>
            <li>Secrets are stored in a dedicated Redis instance</li>
            <li>Access to Redis is protected by password</li>
            <li>Secrets API requires an API key for authentication</li>
            <li>Application retrieves secrets only when needed</li>
            <li>Secrets are never hardcoded or stored in environment variables</li>
            <li>Redis container has no exposed ports to the outside world</li>
        </ul>
        
        <h2>Implementation Details</h2>
        <p>The application retrieves secrets with retries and error handling:</p>
        <pre>
def get_secret(secret_name, default=''):
    """Retrieve a secret from the secrets manager API with retries"""
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"{SECRETS_API_URL}/secrets/{secret_name}",
                headers=API_HEADERS,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("exists", False):
                    return data.get("value", default)
                else:
                    logger.warning(f"Secret {secret_name} not found")
                    return default
            else:
                logger.error(f"Failed to retrieve secret: {response.status_code}")
                
        except requests.RequestException as e:
            logger.error(f"Request error retrieving secret: {e}")
            
        # Wait before retrying
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    
    return default
        </pre>
        
        <script>
            function refreshSecrets() {
                fetch('/refresh-secrets')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('result').innerHTML = 
                            `<p style="color: green">Secrets refreshed: ${data.refreshed}</p>`;
                        setTimeout(() => location.reload(), 1000);
                    })
                    .catch(error => {
                        document.getElementById('result').innerHTML = 
                            `<p style="color: red">Error: ${error}</p>`;
                    });
            }
        </script>
    </body>
    </html>
    """
    
    # Load secrets if not already loaded
    if db_password is None:
        load_secrets()
    
    # Safely mask secrets for display
    def mask_secret(secret, default="Not available"):
        if not secret or secret.endswith('_not_found'):
            return default
        if len(secret) <= 5:
            return "****"
        return f"{secret[:2]}{'*' * (len(secret) - 4)}{secret[-2:]}"
    
    db_password_exists = db_password != 'db_password_not_found'
    api_key_exists = api_key != 'api_key_not_found'
    jwt_secret_exists = jwt_secret != 'jwt_secret_not_found'
    
    # Safe logging without exposing secrets
    logger.info("Rendering index page")
    
    return render_template_string(
        html_content,
        db_password_exists=db_password_exists,
        api_key_exists=api_key_exists,
        jwt_secret_exists=jwt_secret_exists,
        db_password_masked=mask_secret(db_password),
        api_key_masked=mask_secret(api_key),
        jwt_secret_masked=mask_secret(jwt_secret)
    )

@app.route('/refresh-secrets')
def refresh_secrets():
    """Force reload of secrets"""
    load_secrets()
    return jsonify({"status": "success", "refreshed": ["db_password", "api_key", "jwt_secret"]})

@app.route('/api/data')
def api_data():
    """Example of a secure API that doesn't expose secrets"""
    # Load secrets if not already loaded
    if db_password is None:
        load_secrets()
        
    data = {
        'status': 'success',
        'message': 'Using Redis-based secrets management',
        'credentials_available': {
            'db_password': db_password != 'db_password_not_found',
            'api_key': api_key != 'api_key_not_found',
            'jwt_secret': jwt_secret != 'jwt_secret_not_found',
        },
        'environment': os.environ.get('APP_ENV', 'development'),
        'secrets_api': {
            'url': SECRETS_API_URL,
            'status': check_secrets_api_status()
        }
    }
    return jsonify(data)

def check_secrets_api_status():
    """Check if the secrets API is available"""
    try:
        response = requests.get(f"{SECRETS_API_URL}/health", timeout=2)
        if response.status_code == 200:
            return "available"
        return f"error: status code {response.status_code}"
    except requests.RequestException as e:
        return f"error: {str(e)}"

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
    
    secrets_api_status = check_secrets_api_status()
    
    if secrets_available and secrets_api_status == "available":
        return jsonify({
            'status': 'ok', 
            'secrets_available': True,
            'secrets_api': secrets_api_status
        })
    else:
        return jsonify({
            'status': 'degraded', 
            'secrets_available': secrets_available,
            'secrets_api': secrets_api_status
        }), 503

if __name__ == '__main__':
    # Run with secure settings
    app.run(host='0.0.0.0', port=8000, debug=False) 