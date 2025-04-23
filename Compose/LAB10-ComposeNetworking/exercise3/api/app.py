import os
import socket
import time
from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Get instance ID from environment or generate a unique ID
INSTANCE_ID = os.environ.get('INSTANCE_ID', str(time.time())[-5:])
HOSTNAME = socket.gethostname()

class HelloResource(Resource):
    def get(self):
        return {
            "message": "Hello from API service",
            "instance_id": INSTANCE_ID,
            "hostname": HOSTNAME,
            "ip": socket.gethostbyname(HOSTNAME)
        }

class TimeResource(Resource):
    def get(self):
        return {
            "time": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "instance_id": INSTANCE_ID,
            "hostname": HOSTNAME
        }

class NetworkInfoResource(Resource):
    def get(self):
        # Get all network interfaces
        import netifaces
        interfaces = {}
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                interfaces[iface] = addrs[netifaces.AF_INET][0]['addr']
        
        return {
            "instance_id": INSTANCE_ID,
            "hostname": HOSTNAME,
            "ip": socket.gethostbyname(HOSTNAME),
            "interfaces": interfaces
        }

class HealthResource(Resource):
    def get(self):
        return {
            "status": "healthy",
            "instance_id": INSTANCE_ID,
            "hostname": HOSTNAME
        }

# Register resources
api.add_resource(HelloResource, '/')
api.add_resource(TimeResource, '/time')
api.add_resource(NetworkInfoResource, '/network-info')
api.add_resource(HealthResource, '/health')

if __name__ == '__main__':
    # Add a small random sleep to simulate different startup times
    time.sleep(float(INSTANCE_ID) / 100)
    print(f"Starting API instance {INSTANCE_ID} on {HOSTNAME}")
    app.run(host='0.0.0.0', port=8000, debug=True) 