import os
import json
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

# Try to load environment variables from .env file
# Note: In Docker this is usually handled by docker-compose,
# but the dotenv package shows how to do it in Python directly
load_dotenv()

# Application settings
app_name = os.environ.get('APP_NAME', 'Environment Configuration Demo')
app_env = os.environ.get('APP_ENV', 'local')
debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
log_level = os.environ.get('LOG_LEVEL', 'info')

# Database settings
db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'app')
db_user = os.environ.get('DB_USER', 'user')
db_password = os.environ.get('DB_PASSWORD', '')  # Don't print this!
db_port = os.environ.get('DB_PORT', '5432')

# Feature flags
feature_a = os.environ.get('FEATURE_A_ENABLED', 'false').lower() == 'true'
feature_b = os.environ.get('FEATURE_B_ENABLED', 'false').lower() == 'true'

# UI Configuration
theme = os.environ.get('THEME', 'light')
show_admin = os.environ.get('SHOW_ADMIN_FEATURES', 'false').lower() == 'true'

# Environment-specific features
enable_profiler = os.environ.get('ENABLE_PROFILER', 'false').lower() == 'true'
enable_mock = os.environ.get('ENABLE_MOCK_DATA', 'false').lower() == 'true'
enable_caching = os.environ.get('ENABLE_CACHING', 'false').lower() == 'true'
rate_limit = int(os.environ.get('RATE_LIMIT', '10'))
session_timeout = int(os.environ.get('SESSION_TIMEOUT', '1800'))

@app.route('/')
def index():
    # Grouped configuration to display
    app_config = {
        'APP_NAME': app_name,
        'APP_ENV': app_env,
        'DEBUG': debug_mode,
        'LOG_LEVEL': log_level
    }
    
    db_config = {
        'DB_HOST': db_host,
        'DB_NAME': db_name,
        'DB_USER': db_user,
        'DB_PASSWORD': '********',  # Masked for security
        'DB_PORT': db_port
    }
    
    feature_config = {
        'FEATURE_A_ENABLED': feature_a,
        'FEATURE_B_ENABLED': feature_b
    }
    
    ui_config = {
        'THEME': theme,
        'SHOW_ADMIN_FEATURES': show_admin
    }
    
    env_specific = {}
    
    if app_env == 'development':
        env_specific = {
            'ENABLE_PROFILER': enable_profiler,
            'ENABLE_MOCK_DATA': enable_mock
        }
    elif app_env == 'production':
        env_specific = {
            'ENABLE_CACHING': enable_caching,
            'RATE_LIMIT': rate_limit,
            'SESSION_TIMEOUT': session_timeout
        }
    
    return render_template('index.html', 
                         app_name=app_name, 
                         app_env=app_env,
                         debug_mode=debug_mode,
                         log_level=log_level,
                         app_config=app_config,
                         db_config=db_config,
                         feature_config=feature_config,
                         ui_config=ui_config,
                         env_specific=env_specific,
                         theme=theme)

@app.route('/config')
def config():
    # Return configuration as JSON for API clients
    # Mask sensitive data
    config_data = {
        'application': {
            'name': app_name,
            'environment': app_env,
            'debug_enabled': debug_mode,
            'log_level': log_level
        },
        'database': {
            'host': db_host,
            'name': db_name,
            'user': db_user,
            'port': db_port
            # password intentionally omitted
        },
        'features': {
            'feature_a': feature_a,
            'feature_b': feature_b
        },
        'ui': {
            'theme': theme,
            'show_admin': show_admin
        }
    }
    
    if app_env == 'development':
        config_data['development'] = {
            'profiler': enable_profiler,
            'mock_data': enable_mock
        }
    elif app_env == 'production':
        config_data['production'] = {
            'caching': enable_caching,
            'rate_limit': rate_limit,
            'session_timeout': session_timeout
        }
    
    return jsonify(config_data)

if __name__ == '__main__':
    # Configure Flask based on environment variables
    app.debug = debug_mode
    
    # Print startup configuration
    print(f"Starting {app_name}")
    print(f"Environment: {app_env}")
    print(f"Debug Mode: {debug_mode}")
    print(f"Log Level: {log_level}")
    print(f"Theme: {theme}")
    
    app.run(host='0.0.0.0', port=8080) 