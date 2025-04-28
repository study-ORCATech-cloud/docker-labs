from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from Docker!</h1><p>This is a simple Flask application running in a Docker container.</p>"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# TODO: Add a new endpoint that returns the container's hostname
# HINT: Use the socket.gethostname() function to get the hostname
# The endpoint should be accessible at '/hostname' and return JSON like {"hostname": "<container-id>"}

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000) 