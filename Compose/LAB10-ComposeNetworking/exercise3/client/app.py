import os
import socket
import json
import time
import random
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# API service configuration with multiple endpoints for discovery
api_hostname = os.environ.get('API_HOST', 'api')
api_alias = os.environ.get('API_ALIAS', 'api-service')
api_port = os.environ.get('API_PORT', '8000')

# List to store response history
request_history = []

def make_api_request(hostname, endpoint='/'):
    """Helper function to make API request with error handling"""
    url = f"http://{hostname}:{api_port}{endpoint}"
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=2)
        end_time = time.time()
        
        if response.status_code == 200:
            result = {
                "status": "success",
                "target": hostname,
                "endpoint": endpoint,
                "time": time.strftime("%H:%M:%S"),
                "response_time": round((end_time - start_time) * 1000, 2),
                "data": response.json(),
                "ip": socket.gethostbyname(hostname)
            }
        else:
            result = {
                "status": "error",
                "target": hostname,
                "endpoint": endpoint,
                "time": time.strftime("%H:%M:%S"),
                "error": f"HTTP {response.status_code}"
            }
    except requests.RequestException as e:
        result = {
            "status": "error",
            "target": hostname,
            "endpoint": endpoint,
            "time": time.strftime("%H:%M:%S"),
            "error": str(e)
        }
    except socket.gaierror:
        result = {
            "status": "error",
            "target": hostname,
            "endpoint": endpoint,
            "time": time.strftime("%H:%M:%S"),
            "error": f"Cannot resolve hostname: {hostname}"
        }
    
    # Add to history and limit size
    request_history.append(result)
    if len(request_history) > 20:
        request_history.pop(0)
    
    return result

@app.route('/')
def index():
    # Make a request using primary hostname
    primary_result = make_api_request(api_hostname)
    
    # Make a request using alias
    alias_result = make_api_request(api_alias)
    
    # Get hostname resolution info
    hostname_info = {}
    for host in [api_hostname, api_alias]:
        try:
            ip = socket.gethostbyname(host)
            hostname_info[host] = {
                "resolved": True,
                "ip": ip
            }
        except socket.gaierror:
            hostname_info[host] = {
                "resolved": False,
                "error": "Cannot resolve hostname"
            }
    
    return render_template('index.html',
                          primary_result=primary_result,
                          alias_result=alias_result,
                          hostname_info=hostname_info,
                          history=request_history)

@app.route('/api-request/<hostname>')
def api_request(hostname):
    """Make a request to a specific API hostname and return result"""
    result = make_api_request(hostname)
    return jsonify(result)

@app.route('/api-request/<hostname>/<path:endpoint>')
def api_request_endpoint(hostname, endpoint):
    """Make a request to a specific API hostname and endpoint"""
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    result = make_api_request(hostname, endpoint)
    return jsonify(result)

@app.route('/multi-request')
def multi_request():
    """Make multiple requests to demonstrate load balancing"""
    results = []
    
    # Make 5 requests to the service using the primary hostname
    for _ in range(5):
        result = make_api_request(api_hostname)
        results.append(result)
        time.sleep(0.1)  # Small delay to avoid flooding
    
    return jsonify(results)

@app.route('/health')
def health():
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    return jsonify({
        "status": "healthy",
        "service": "client",
        "hostname": hostname,
        "ip": container_ip
    })

@app.route('/dns-lookup/<hostname>')
def dns_lookup(hostname):
    """Look up a hostname and return the IP address"""
    try:
        ip = socket.gethostbyname(hostname)
        return jsonify({
            "hostname": hostname,
            "ip": ip,
            "resolved": True
        })
    except socket.gaierror:
        return jsonify({
            "hostname": hostname,
            "resolved": False,
            "error": "Cannot resolve hostname"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 