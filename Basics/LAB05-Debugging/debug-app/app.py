from flask import Flask, jsonify, request
import os
import time
import random
import threading
import logging

app = Flask(__name__)

# Configure logging (BUG 1: Incorrect log directory)
log_dir = "/tmp/logs"  # This directory doesn't exist in the container by default
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f"{log_dir}/app.log"  # This will cause an error
)

# BUG 2: Memory leak simulation
memory_hog = []

# BUG 3: Race condition with a shared counter
counter = 0
counter_lock = None  # Should be a threading.Lock() but it's not initialized

# BUG 4: This will cause a port conflict when running in a container
PORT = 8080  # Dockerfile exposes 5000, but the app runs on 8080

# BUG 5: Unreachable endpoint due to incorrect path
@app.route('/api/v1/health')  # Should be just /health for simplicity
def health():
    return jsonify({"status": "healthy"})

@app.route('/')
def home():
    global counter
    # BUG 6: Incrementing counter without lock protection
    counter += 1
    return f"Welcome to the Debug App! Counter: {counter}"

# BUG 7: This endpoint leaks memory
@app.route('/memory-leak')
def memory_leak():
    global memory_hog
    # Adding 1MB of data on each request
    memory_hog.append('x' * 1024 * 1024)
    return jsonify({"message": "Added 1MB to memory", "total_leaks": len(memory_hog)})

# BUG 8: This endpoint sometimes crashes
@app.route('/unstable')
def unstable():
    if random.randint(1, 3) == 1:
        # Simulate a crash
        raise Exception("Random crash occurred!")
    return jsonify({"message": "Lucky! No crash this time."})

# BUG 9: This endpoint is slow and blocks the server
@app.route('/slow')
def slow():
    # Blocking sleep - this will block the entire server
    time.sleep(10)
    return jsonify({"message": "Finally responded after 10 seconds"})

# BUG 10: Missing environment variable
@app.route('/config')
def config():
    # Will raise KeyError when API_KEY environment variable is not set
    api_key = os.environ['API_KEY']
    return jsonify({"api_key": api_key})

# Added a few working endpoints for comparison
@app.route('/working')
def working():
    return jsonify({"message": "This endpoint works properly!"})

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify(data)

if __name__ == '__main__':
    print(f"Starting Flask app on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True) 