import os
import socket
import requests
from flask import Flask, request, jsonify, Response, stream_with_context

app = Flask(__name__)

# Service configurations
users_service_host = os.environ.get('USERS_SERVICE_HOST', 'users-service')
users_service_port = os.environ.get('USERS_SERVICE_PORT', '8000')
users_service_url = f"http://{users_service_host}:{users_service_port}"

products_service_host = os.environ.get('PRODUCTS_SERVICE_HOST', 'products-service')
products_service_port = os.environ.get('PRODUCTS_SERVICE_PORT', '8000')
products_service_url = f"http://{products_service_host}:{products_service_port}"

@app.route('/')
def index():
    hostname = socket.gethostname()
    return jsonify({
        "service": "API Gateway",
        "hostname": hostname,
        "endpoints": [
            {
                "path": "/users",
                "description": "User service endpoints",
                "service": users_service_url
            },
            {
                "path": "/products",
                "description": "Product service endpoints",
                "service": products_service_url
            },
            {
                "path": "/network-info",
                "description": "Network information"
            }
        ]
    })

@app.route('/users', defaults={'path': ''})
@app.route('/users/<path:path>')
def proxy_users(path):
    """Proxy requests to the users service"""
    return proxy_request(f"{users_service_url}/{path}", request)

@app.route('/products', defaults={'path': ''})
@app.route('/products/<path:path>')
def proxy_products(path):
    """Proxy requests to the products service"""
    return proxy_request(f"{products_service_url}/{path}", request)

def proxy_request(url, req):
    """Forward requests to the appropriate service"""
    # Copy request headers
    headers = {key: value for (key, value) in req.headers if key != 'Host'}
    
    # Determine request method and parameters
    if req.method == 'GET':
        resp = requests.get(url, headers=headers, params=req.args, stream=True)
    elif req.method == 'POST':
        resp = requests.post(url, headers=headers, json=req.get_json(), stream=True)
    elif req.method == 'PUT':
        resp = requests.put(url, headers=headers, json=req.get_json(), stream=True)
    elif req.method == 'DELETE':
        resp = requests.delete(url, headers=headers, stream=True)
    else:
        return jsonify({"error": "Method not supported"}), 405
    
    # Stream response from service
    response = Response(stream_with_context(resp.iter_content(chunk_size=1024)),
                       content_type=resp.headers.get('content-type', 'application/json'))
    
    # Copy response headers
    for key, value in resp.headers.items():
        if key.lower() not in ('content-encoding', 'transfer-encoding', 'content-length'):
            response.headers[key] = value
            
    # Add gateway info to headers
    response.headers['X-Gateway'] = socket.gethostname()
    
    return response, resp.status_code

@app.route('/network-info')
def network_info():
    """Get network information about the gateway and services"""
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    # Check connectivity to services
    users_status = check_service_connectivity(users_service_host, users_service_port)
    products_status = check_service_connectivity(products_service_host, products_service_port)
    
    # Get all network interfaces
    import netifaces
    interfaces = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            interfaces[iface] = addrs[netifaces.AF_INET][0]['addr']
    
    return jsonify({
        "service": "gateway",
        "hostname": hostname,
        "ip": container_ip,
        "interfaces": interfaces,
        "connectivity": {
            "users_service": users_status,
            "products_service": products_status
        }
    })

def check_service_connectivity(host, port):
    """Check if a service is reachable"""
    try:
        # Try to resolve hostname
        ip = socket.gethostbyname(host)
        
        # Try to connect to service
        try:
            response = requests.get(f"http://{host}:{port}/health", timeout=1)
            if response.status_code == 200:
                return {
                    "status": "connected",
                    "ip": ip,
                    "details": response.json()
                }
            else:
                return {
                    "status": "error",
                    "ip": ip,
                    "error": f"HTTP {response.status_code}"
                }
        except requests.RequestException as e:
            return {
                "status": "unreachable",
                "ip": ip,
                "error": str(e)
            }
    except socket.gaierror:
        return {
            "status": "dns_error",
            "error": f"Cannot resolve hostname: {host}"
        }

@app.route('/health')
def health():
    hostname = socket.gethostname()
    return jsonify({
        "status": "healthy",
        "service": "gateway",
        "hostname": hostname
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 