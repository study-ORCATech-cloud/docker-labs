from flask import Flask, send_file
import os
import socket
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/container-info')
def container_info():
    hostname = socket.gethostname()
    info = f"Hostname: {hostname}\n"
    
    try:
        # Try to get container ID - this will only work inside Docker
        result = subprocess.run(
            ["cat /proc/self/cgroup | grep -o -E '([0-9a-f]{64})' | head -n 1"],
            shell=True, 
            capture_output=True, 
            text=True
        )
        container_id = result.stdout.strip()
        if container_id:
            info += f"Container ID: {container_id[:12]}"
        else:
            info += "Container ID: Not running in Docker"
    except Exception as e:
        info += f"Container ID: Not running in Docker (Error: {str(e)})"
    
    return info

if __name__ == '__main__':
    print("Server running at http://0.0.0.0:80/")
    print("Docker Getting Started Lab is ready!")
    app.run(host='0.0.0.0', port=80) 