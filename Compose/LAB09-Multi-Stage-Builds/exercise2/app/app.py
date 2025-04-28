#!/usr/bin/env python3
"""
Advanced Flask application demonstrating multi-stage builds
with dependency management and environment-specific configuration
"""
import os
import platform
import sys
import time
from datetime import datetime
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string, request

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure app based on environment
BUILD_ENV = os.environ.get('BUILD_ENV', 'development')
if BUILD_ENV == 'development':
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    # Only activate the debug toolbar in development
    try:
        from flask_debugtoolbar import DebugToolbarExtension
        app.config['SECRET_KEY'] = 'development-secret-key'
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        toolbar = DebugToolbarExtension(app)
        logger.info("Debug toolbar enabled")
    except ImportError:
        logger.warning("Debug toolbar not available")
else:
    app.config['DEBUG'] = False
    app.config['ENV'] = 'production'

# HTML Template with more sophisticated UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Advanced Multi-Stage Build Demo</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background-color: #f9f9f9;
        }
        .container {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .info {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #17a2b8;
        }
        .env {
            border-left: 4px solid #28a745;
        }
        .sys {
            border-left: 4px solid #007bff;
        }
        .dev {
            border-left: 4px solid #ffc107;
        }
        h1 {
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        h2 {
            color: #444;
            margin-top: 25px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: Consolas, monospace;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .badge {
            display: inline-block;
            padding: 0.25em 0.6em;
            font-size: 0.75em;
            font-weight: bold;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.25rem;
            color: white;
            margin-left: 5px;
        }
        .badge-dev {
            background-color: #28a745;
        }
        .badge-prod {
            background-color: #dc3545;
        }
        .footer {
            margin-top: 30px;
            color: #777;
            font-size: 0.9em;
            text-align: center;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .timestamp {
            font-size: 0.9em;
            color: #666;
        }
        .button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .button:hover {
            background-color: #0069d9;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Advanced Multi-Stage Build Demo</h1>
        <div class="timestamp">{{ current_time }}</div>
    </div>
    
    <div class="info">
        <p>This is an advanced Flask application demonstrating Docker multi-stage builds with proper dependency management.</p>
        <p>Build environment: <strong>{{ build_env }}</strong> 
            <span class="badge {% if build_env == 'development' %}badge-dev{% else %}badge-prod{% endif %}">
                {{ build_env }}
            </span>
        </p>
    </div>
    
    <div class="container env">
        <h2>Environment Information</h2>
        <table>
            <tr>
                <th>Variable</th>
                <th>Value</th>
            </tr>
            {% for key, value in env_vars.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ value }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    
    <div class="container sys">
        <h2>System Information</h2>
        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
            {% for key, value in sys_info.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ value }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    
    {% if build_env == 'development' %}
    <div class="container dev">
        <h2>Development Tools</h2>
        <p>The following development tools are installed in this environment:</p>
        <table>
            <tr>
                <th>Package</th>
                <th>Version</th>
            </tr>
            {% for package in dev_packages %}
            <tr>
                <td>{{ package.name }}</td>
                <td>{{ package.version }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    {% endif %}
    
    <div class="container">
        <h2>Python Packages</h2>
        <p>Total packages installed: <strong>{{ python_packages|length }}</strong></p>
        <button class="button" onclick="toggleTable()">Show/Hide Packages</button>
        <div id="packagesTable" style="display: none; margin-top: 15px;">
            <table>
                <tr>
                    <th>Package</th>
                    <th>Version</th>
                </tr>
                {% for package in python_packages %}
                <tr>
                    <td>{{ package.name }}</td>
                    <td>{{ package.version }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
    
    <div class="container" style="text-align: center; margin-top: 20px;">
        <button class="button" onclick="refreshPage()">Refresh Data</button>
    </div>

    <div class="footer">
        <p>Advanced Multi-Stage Build Demo | LAB09-MultiStageBuilds | {{ build_date }}</p>
    </div>
    
    <script>
        function toggleTable() {
            var table = document.getElementById('packagesTable');
            table.style.display = table.style.display === 'none' ? 'block' : 'none';
        }
        
        function refreshPage() {
            window.location.reload();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page with system and environment information"""
    import pkg_resources
    
    # Collect environment variables
    env_vars = {
        'APP_ENV': os.environ.get('APP_ENV', 'Not set'),
        'BUILD_ENV': os.environ.get('BUILD_ENV', 'Not set'),
        'HOSTNAME': os.environ.get('HOSTNAME', 'Not set'),
        'PYTHON_VERSION': platform.python_version(),
        'FLASK_ENV': os.environ.get('FLASK_ENV', 'Not set'),
        'FLASK_DEBUG': os.environ.get('FLASK_DEBUG', 'Not set')
    }
    
    # Collect system information
    sys_info = {
        'Platform': platform.platform(),
        'System': platform.system(),
        'Machine': platform.machine(),
        'Python Path': sys.prefix,
        'Current Directory': os.getcwd(),
        'Process ID': os.getpid(),
        'Current Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Collect installed Python packages
    all_packages = [
        {'name': pkg.key, 'version': pkg.version}
        for pkg in sorted(pkg_resources.working_set, key=lambda x: x.key)
    ]
    
    # Identify development packages
    dev_packages = []
    if BUILD_ENV == 'development':
        dev_package_names = [
            'pytest', 'flask-debugtoolbar', 'black', 'flake8', 
            'isort', 'coverage'
        ]
        dev_packages = [
            pkg for pkg in all_packages 
            if pkg['name'] in dev_package_names
        ]
    
    return render_template_string(
        HTML_TEMPLATE,
        build_env=BUILD_ENV,
        env_vars=env_vars,
        sys_info=sys_info,
        python_packages=all_packages,
        dev_packages=dev_packages,
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        build_date=datetime.now().strftime('%Y-%m-%d')
    )

@app.route('/api/info')
def api_info():
    """API endpoint returning system and environment information as JSON"""
    return jsonify({
        'env': {
            'APP_ENV': os.environ.get('APP_ENV', 'Not set'),
            'BUILD_ENV': os.environ.get('BUILD_ENV', 'Not set'),
            'PYTHON_VERSION': platform.python_version(),
            'FLASK_ENV': os.environ.get('FLASK_ENV', 'Not set')
        },
        'system': {
            'platform': platform.platform(),
            'python_implementation': platform.python_implementation(),
            'python_version': platform.python_version(),
            'timestamp': datetime.now().isoformat()
        }
    })

@app.route('/api/simulate-load')
def simulate_load():
    """Simulate CPU load for testing"""
    duration = request.args.get('duration', default=1, type=int)
    # Limit max duration to 10 seconds for safety
    duration = min(duration, 10)
    
    logger.info(f"Simulating CPU load for {duration} seconds")
    start_time = time.time()
    # Simple CPU-intensive operation
    while time.time() - start_time < duration:
        _ = [i**2 for i in range(10000)]
    
    end_time = time.time()
    return jsonify({
        'status': 'success',
        'duration': end_time - start_time,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'build_env': BUILD_ENV,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    logger.info(f"Starting application in {BUILD_ENV} mode")
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG']) 