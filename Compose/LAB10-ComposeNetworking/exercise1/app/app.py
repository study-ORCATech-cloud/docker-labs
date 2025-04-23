import os
import socket
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Configure Redis connection
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# Connect to Redis
import redis
redis_client = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def index():
    # Increment counter
    counter = redis_client.incr('visits')
    
    # Get hostname and IP address for network demonstration
    hostname = socket.gethostname()
    try:
        redis_ip = socket.gethostbyname(redis_host)
    except socket.gaierror:
        redis_ip = "Unable to resolve"
    
    # Get container's own IP
    container_ip = socket.gethostbyname(hostname)
    
    return render_template('index.html', 
                           counter=counter, 
                           hostname=hostname,
                           container_ip=container_ip,
                           redis_host=redis_host,
                           redis_ip=redis_ip)

@app.route('/network-info')
def network_info():
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    # Try to resolve Redis host to demonstrate DNS service discovery
    try:
        redis_ip = socket.gethostbyname(redis_host)
        redis_reachable = True
    except socket.gaierror:
        redis_ip = "Unable to resolve"
        redis_reachable = False
    
    # Check if Redis is reachable by trying to ping it
    try:
        redis_client.ping()
        redis_status = "Connected"
    except:
        redis_status = "Not connected"
    
    # Get interface information
    import netifaces
    interfaces = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            interfaces[iface] = addrs[netifaces.AF_INET][0]['addr']
    
    return jsonify({
        "container": {
            "hostname": hostname,
            "ip": container_ip,
            "interfaces": interfaces
        },
        "redis": {
            "hostname": redis_host,
            "ip": redis_ip,
            "reachable": redis_reachable,
            "status": redis_status,
            "port": redis_port
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 