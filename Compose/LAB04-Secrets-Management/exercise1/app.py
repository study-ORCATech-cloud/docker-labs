from flask import Flask, jsonify, render_template_string
import os
import logging

# Insecure: Hardcoded credentials in the source code
HARDCODED_PASSWORD = "source_code_password_123"
HARDCODED_API_KEY = "source_code_api_key_456"

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Insecure: Log setup that might leak secrets
logger.info(f"Starting application with API_KEY: {os.environ.get('API_KEY')}")
logger.info(f"Database password length: {len(os.environ.get('DB_PASSWORD', ''))}")

@app.route('/')
def index():
    """Display information about secrets handling (insecurely)"""
    # This template exposes secrets directly to the browser
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Insecure Secrets Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #d9534f;
                border-bottom: 2px solid #d9534f;
                padding-bottom: 10px;
            }
            .warning {
                background-color: #fff3cd;
                border: 1px solid #ffeeba;
                color: #856404;
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
        </style>
    </head>
    <body>
        <h1>Insecure Secrets Management Demo</h1>
        
        <div class="warning">
            <strong>Warning:</strong> This page intentionally demonstrates INSECURE practices.
            Do NOT use these methods in real applications.
        </div>
        
        <h2>Exposed Secrets</h2>
        <table class="secret-table">
            <tr>
                <th>Secret Type</th>
                <th>Source</th>
                <th>Value (EXPOSED!)</th>
            </tr>
            <tr>
                <td>Database Password</td>
                <td>Environment Variable</td>
                <td>{{ db_password }}</td>
            </tr>
            <tr>
                <td>API Key</td>
                <td>Environment Variable</td>
                <td>{{ api_key }}</td>
            </tr>
            <tr>
                <td>JWT Secret</td>
                <td>Environment Variable</td>
                <td>{{ jwt_secret }}</td>
            </tr>
            <tr>
                <td>Backup DB Password</td>
                <td>Dockerfile ENV</td>
                <td>{{ backup_db_password }}</td>
            </tr>
            <tr>
                <td>Backup API Key</td>
                <td>Dockerfile ENV</td>
                <td>{{ backup_api_key }}</td>
            </tr>
            <tr>
                <td>Hardcoded Password</td>
                <td>Source Code</td>
                <td>{{ hardcoded_password }}</td>
            </tr>
            <tr>
                <td>Hardcoded API Key</td>
                <td>Source Code</td>
                <td>{{ hardcoded_api_key }}</td>
            </tr>
        </table>
        
        <h2>Security Issues Demonstrated</h2>
        <ul>
            <li>Hardcoded credentials in source code</li>
            <li>Credentials in environment variables (visible in 'docker inspect')</li>
            <li>Credentials hardcoded in Dockerfile (persisted in image layers)</li>
            <li>Logging sensitive information</li>
            <li>Exposing secrets to frontend/browser</li>
            <li>No encryption or access control for secrets</li>
        </ul>
        
        <h2>Better Alternatives</h2>
        <ul>
            <li>Use Docker Secrets (for Swarm mode)</li>
            <li>Mount sensitive files with proper permissions</li>
            <li>Use a secrets management service</li>
            <li>Never log credentials or expose them to browsers</li>
            <li>Keep secrets out of source code and Dockerfiles</li>
        </ul>
        
        <div class="source">
            Continue to <a href="/api/data">API endpoint</a> to see more issues.
        </div>
    </body>
    </html>
    """
    
    # Get all the sensitive information to render in the template
    db_password = os.environ.get('DB_PASSWORD', '')
    api_key = os.environ.get('API_KEY', '')
    jwt_secret = os.environ.get('JWT_SECRET', '')
    backup_db_password = os.environ.get('BACKUP_DB_PASSWORD', '')
    backup_api_key = os.environ.get('BACKUP_API_KEY', '')
    
    # Insecure: Logging secrets
    logger.info("Rendering index page with secrets information")
    
    return render_template_string(
        html_content,
        db_password=db_password,
        api_key=api_key,
        jwt_secret=jwt_secret,
        backup_db_password=backup_db_password,
        backup_api_key=backup_api_key,
        hardcoded_password=HARDCODED_PASSWORD,
        hardcoded_api_key=HARDCODED_API_KEY
    )

@app.route('/api/data')
def api_data():
    # Insecure: Including secrets in API responses
    data = {
        'status': 'success',
        'message': 'This API response contains sensitive information',
        'connection_string': f'postgresql://admin:{os.environ.get("DB_PASSWORD")}@db:5432/app',
        'api_auth': f'Bearer {os.environ.get("API_KEY")}',
        'debug_info': {
            'env_vars': dict(os.environ),  # Insecure: Exposing all environment variables
        }
    }
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    # Insecure: Potentially exposing application on all interfaces in debug mode
    app.run(host='0.0.0.0', port=8000, debug=debug_mode) 