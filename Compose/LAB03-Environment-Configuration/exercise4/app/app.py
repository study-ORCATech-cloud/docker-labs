import os
import json
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)

# Get the environment or default to development
APP_ENV = os.getenv("APP_ENV", "development")
APP_NAME = os.getenv("APP_NAME", "Flask Config Demo")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ('true', '1', 't', 'yes')

# Function to read Docker secrets
def get_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as secret_file:
            return secret_file.read().rstrip('\n')
    except IOError:
        return None

# Function to mask sensitive information
def mask_sensitive(value):
    if value is None:
        return 'Not configured'
    
    # If the value appears to be JSON, we just indicate it's present without showing content
    if value.startswith('{') and value.endswith('}'):
        return 'JSON data [MASKED]'
    
    # For other types, mask all but first and last characters
    if len(value) <= 4:
        return '****'  # Too short to show anything
    
    return value[0] + '*' * (len(value) - 2) + value[-1]

@app.route('/')
def index():
    # Prepare configuration dictionaries for the template
    public_config = {
        'APP_NAME': APP_NAME,
        'APP_ENV': APP_ENV,
        'HOST': os.getenv('HOST', '0.0.0.0'),
        'PORT': os.getenv('PORT', '8080'),
        'DEBUG_MODE': str(DEBUG_MODE),
    }
    
    # Define known secrets
    secret_keys = ['DB_PASSWORD', 'API_KEY', 'JWT_SECRET']
    
    # Check if secrets directory exists
    has_secrets = os.path.exists('/run/secrets')
    
    # Get secure config (via Docker secrets)
    secure_config = {}
    if has_secrets:
        for key in secret_keys:
            value = get_secret(key.lower())
            if value:
                secure_config[key] = mask_sensitive(value)
    
    # Get insecure config (environment variables that should be secrets)
    insecure_config = {}
    for key in secret_keys:
        value = os.getenv(key)
        if value:
            insecure_config[key] = mask_sensitive(value)
    
    # Additional public config from environment
    for key, value in os.environ.items():
        if key.startswith('PUBLIC_'):
            public_config[key] = value
    
    return render_template('index.html', 
                           app_name=APP_NAME,
                           app_env=APP_ENV,
                           debug_mode=DEBUG_MODE,
                           has_secrets=has_secrets,
                           public_config=public_config,
                           secure_config=secure_config,
                           insecure_config=insecure_config)

@app.route('/info')
def info():
    # Returns non-sensitive information as JSON
    info_data = {
        'app_name': APP_NAME,
        'environment': APP_ENV,
        'debug_mode': DEBUG_MODE,
        'has_secrets': os.path.exists('/run/secrets'),
        'public_variables': {k: v for k, v in os.environ.items() if k.startswith('PUBLIC_')}
    }
    return jsonify(info_data)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    debug = DEBUG_MODE
    
    print(f"Starting {APP_NAME} in {APP_ENV} environment")
    app.run(host=host, port=port, debug=debug) 