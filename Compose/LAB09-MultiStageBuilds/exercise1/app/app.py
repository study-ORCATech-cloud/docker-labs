#!/usr/bin/env python3
"""
Simple Flask application for demonstrating multi-stage builds
"""
import os
import platform
import sys
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Stage Build Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-top: 20px;
        }
        .info {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .env {
            background-color: #e9f7ef;
        }
        .sys {
            background-color: #eaf2f8;
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
            font-family: monospace;
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
        .footer {
            margin-top: 30px;
            color: #777;
            font-size: 0.9em;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Multi-Stage Build Demo Application</h1>
    
    <div class="info">
        <p>This is a simple Python Flask application used to demonstrate Docker multi-stage builds.</p>
        <p>Current build type: <strong>{{ build_type }}</strong></p>
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
    
    <div class="container">
        <h2>Python Packages</h2>
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

    <div class="footer">
        <p>Multi-Stage Build Demo | LAB09-MultiStageBuilds</p>
    </div>
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
        'HOSTNAME': os.environ.get('HOSTNAME', 'Not set'),
        'PYTHON_VERSION': platform.python_version(),
        'FLASK_ENV': os.environ.get('FLASK_ENV', 'Not set')
    }
    
    # Collect system information
    sys_info = {
        'Platform': platform.platform(),
        'System': platform.system(),
        'Machine': platform.machine(),
        'Python Path': sys.prefix,
        'Current Directory': os.getcwd()
    }
    
    # Collect installed Python packages
    python_packages = [
        {'name': pkg.key, 'version': pkg.version}
        for pkg in sorted(pkg_resources.working_set, key=lambda x: x.key)
    ]
    
    # Determine build type based on container size
    build_type = "Standard" if os.environ.get('BUILD_TYPE') == 'original' else "Multi-stage"
    
    return render_template_string(
        HTML_TEMPLATE,
        build_type=build_type,
        env_vars=env_vars,
        sys_info=sys_info,
        python_packages=python_packages
    )

@app.route('/api/info')
def api_info():
    """API endpoint returning system and environment information as JSON"""
    return jsonify({
        'env': {
            'APP_ENV': os.environ.get('APP_ENV', 'Not set'),
            'PYTHON_VERSION': platform.python_version(),
            'FLASK_ENV': os.environ.get('FLASK_ENV', 'Not set')
        },
        'system': {
            'platform': platform.platform(),
            'python_implementation': platform.python_implementation(),
            'python_version': platform.python_version()
        },
        'build_type': "Standard" if os.environ.get('BUILD_TYPE') == 'original' else "Multi-stage"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=os.environ.get('FLASK_DEBUG', '0') == '1') 