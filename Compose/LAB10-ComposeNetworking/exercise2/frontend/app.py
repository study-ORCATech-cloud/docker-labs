import os
import socket
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Backend service configuration
backend_host = os.environ.get('BACKEND_HOST', 'backend')
backend_port = os.environ.get('BACKEND_PORT', '8000')
backend_url = f"http://{backend_host}:{backend_port}"

@app.route('/')
def index():
    # Get network information
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    # Try to connect to backend
    backend_status = "Unknown"
    backend_data = []
    backend_ip = "Unknown"
    
    try:
        # Try to resolve backend hostname
        backend_ip = socket.gethostbyname(backend_host)
        
        # Try to get data from backend
        response = requests.get(f"{backend_url}/data", timeout=2)
        if response.status_code == 200:
            backend_status = "Connected"
            backend_data = response.json().get('data', [])
        else:
            backend_status = f"Error: {response.status_code}"
    except socket.gaierror:
        backend_status = "DNS resolution failed"
    except requests.RequestException as e:
        backend_status = f"Connection failed: {str(e)}"
    
    # Try to connect to database (this should fail due to network isolation)
    db_status = "Unknown"
    db_ip = "Unknown"
    
    try:
        # Try to resolve db hostname
        db_ip = socket.gethostbyname('db')
        db_status = "Resolved (should not happen with proper network isolation)"
    except socket.gaierror:
        db_status = "DNS resolution failed (expected with network isolation)"
    
    return render_template('index.html',
                          hostname=hostname,
                          container_ip=container_ip,
                          backend_host=backend_host,
                          backend_ip=backend_ip,
                          backend_status=backend_status,
                          backend_data=backend_data,
                          db_ip=db_ip,
                          db_status=db_status)

@app.route('/network-info')
def network_info():
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    # Test connectivity to backend
    backend_reachable = False
    backend_ip = "Unknown"
    
    try:
        backend_ip = socket.gethostbyname(backend_host)
        response = requests.get(f"{backend_url}/health", timeout=1)
        backend_reachable = response.status_code == 200
    except (socket.gaierror, requests.RequestException):
        pass
    
    # Test connectivity to db (should fail with network isolation)
    db_reachable = False
    db_ip = "Unknown"
    
    try:
        db_ip = socket.gethostbyname('db')
        db_reachable = True  # If we can resolve, we consider it reachable
    except socket.gaierror:
        pass
    
    # Get all network interfaces
    import netifaces
    interfaces = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            interfaces[iface] = addrs[netifaces.AF_INET][0]['addr']
    
    return jsonify({
        "container": {
            "service": "frontend",
            "hostname": hostname,
            "ip": container_ip,
            "interfaces": interfaces
        },
        "connections": {
            "backend": {
                "hostname": backend_host,
                "ip": backend_ip,
                "reachable": backend_reachable
            },
            "db": {
                "hostname": "db",
                "ip": db_ip,
                "reachable": db_reachable
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 