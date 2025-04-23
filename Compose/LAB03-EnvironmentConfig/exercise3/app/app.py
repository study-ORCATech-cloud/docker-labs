import os
import json
import socket
from flask import Flask, render_template, jsonify
from waitress import serve
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables (from .env file if present)
load_dotenv()

# Application settings
app_name = os.environ.get('APP_NAME', 'Multi Environment Demo')
app_env = os.environ.get('APP_ENV', 'development')
debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
log_level = os.environ.get('LOG_LEVEL', 'info')
reload_enabled = os.environ.get('RELOAD', 'false').lower() == 'true'

# Get hostname for container identification
hostname = socket.gethostname()

@app.route('/')
def index():
    # Get all environment variables for display
    filtered_env_vars = {key: value for key, value in os.environ.items() 
                        if not key.startswith('PATH') and not key.startswith('PYTHON')}
    
    # Determine if we're running in dev or prod based on compose file
    # In production, we wouldn't use a bind mount and reload would be disabled
    is_dev_mode = os.path.exists('/app/app.py') and reload_enabled
    
    environment_info = {
        'app_name': app_name,
        'hostname': hostname,
        'environment': app_env,
        'debug_enabled': debug_mode,
        'log_level': log_level,
        'reload_enabled': reload_enabled,
        'is_development_mode': is_dev_mode
    }
    
    return render_template('index.html', 
                         app_name=app_name, 
                         hostname=hostname,
                         app_env=app_env,
                         debug_mode=debug_mode,
                         log_level=log_level,
                         reload_enabled=reload_enabled,
                         is_dev_mode=is_dev_mode,
                         env_vars=filtered_env_vars)

@app.route('/info')
def info():
    # Return basic info about the environment
    info_data = {
        'app_name': app_name,
        'environment': app_env,
        'hostname': hostname,
        'debug_mode': debug_mode,
        'log_level': log_level,
        'reload_enabled': reload_enabled
    }
    return jsonify(info_data)

@app.route('/environment')
def environment():
    # If debug mode is enabled, return all environment variables
    if debug_mode:
        # Filter out some system environment variables
        filtered_env = {k: v for k, v in os.environ.items() if not k.startswith(('PATH', 'PYTHON', 'LD_', 'HOME'))}
        return jsonify(filtered_env)
    else:
        return jsonify({'error': 'Debug mode is disabled. Environment variables are not exposed in production.'}), 403

if __name__ == '__main__':
    print(f"Starting {app_name}")
    print(f"Environment: {app_env}")
    print(f"Debug Mode: {debug_mode}")
    print(f"Log Level: {log_level}")
    print(f"Host: {hostname}")
    
    if app_env == 'development' or debug_mode:
        # Use Flask's development server in development mode
        print("Running with Flask development server")
        app.run(host='0.0.0.0', port=8080, debug=debug_mode)
    else:
        # Use Waitress in production for better performance and security
        print("Running with Waitress production server")
        serve(app, host='0.0.0.0', port=8080) 