from flask import Flask, send_file
import os
import socket
import subprocess

# Initialize Flask app
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return send_file('index.html')

# Route to display container information
@app.route('/container-info')
def container_info():
    # Get container hostname
    hostname = socket.gethostname()
    info = f"Hostname: {hostname}\n"
    
    try:
        # TODO: Implement the code to extract the container ID
        # HINT: You can use the subprocess module to run a shell command
        # that looks for container ID in the cgroup file
        # Example of subprocess usage:
        # result = subprocess.run(["command"], shell=True, capture_output=True, text=True)
        # The command should extract a 64-character hex string from /proc/self/cgroup
        
        # Placeholder until implemented by student
        info += "Container ID: TODO - Implement container ID extraction"
    except Exception as e:
        info += f"Container ID: Not running in Docker (Error: {str(e)})"
    
    return info

# TODO: Add a new route '/env-vars' that returns Docker environment variables
# HINT: Use os.environ to access environment variables
# The route should display at least 3 environment variables

if __name__ == '__main__':
    print("Server running at http://0.0.0.0:80/")
    print("Docker Getting Started Lab is ready!")
    # TODO: Experiment with different port settings
    app.run(host='0.0.0.0', port=80) 