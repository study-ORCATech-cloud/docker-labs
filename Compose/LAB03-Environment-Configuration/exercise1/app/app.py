import os
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Get environment variables with defaults
app_name = os.environ.get('APP_NAME', 'Environment Variables Demo')
app_env = os.environ.get('APP_ENV', 'local')
debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
log_level = os.environ.get('LOG_LEVEL', 'info')

@app.route('/')
def index():
    # Return all environment variables for display
    env_vars = {
        'APP_NAME': app_name,
        'APP_ENV': app_env,
        'DEBUG': debug_mode,
        'LOG_LEVEL': log_level
    }
    
    # Get all environment variables for display
    all_env_vars = {key: value for key, value in os.environ.items() if key.startswith('APP_') or key in ['DEBUG', 'LOG_LEVEL']}
    
    return render_template('index.html', 
                          app_name=app_name, 
                          app_env=app_env, 
                          debug_mode=debug_mode,
                          log_level=log_level,
                          all_env_vars=all_env_vars)

@app.route('/config')
def config():
    # Return configuration as JSON for API clients
    config_data = {
        'app_name': app_name,
        'environment': app_env,
        'debug_enabled': debug_mode,
        'log_level': log_level,
        'all_env_vars': {key: value for key, value in os.environ.items()}
    }
    return jsonify(config_data)

@app.route('/debug')
def debug():
    # Only show detailed debug info if DEBUG is true
    if debug_mode:
        environment_info = {
            'Environment Variables': dict(os.environ),
            'Flask Config': {key: str(value) for key, value in app.config.items()}
        }
        return jsonify(environment_info)
    else:
        return jsonify({'error': 'Debug mode is disabled'}), 403

if __name__ == '__main__':
    # Configure Flask based on environment variables
    app.debug = debug_mode
    
    # Print startup configuration
    print(f"Starting {app_name}")
    print(f"Environment: {app_env}")
    print(f"Debug Mode: {debug_mode}")
    print(f"Log Level: {log_level}")
    
    app.run(host='0.0.0.0', port=8080) 