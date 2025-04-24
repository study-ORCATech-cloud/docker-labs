from flask import Flask, jsonify, request
import os
import time
import random
import threading
import logging

app = Flask(__name__)

# TODO 1: Fix logging configuration
# Problem: Incorrect log directory that doesn't exist in the container
# HINT: Use a directory that exists or ensure it's created
log_dir = "/tmp/logs"  # This directory doesn't exist in the container by default
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f"{log_dir}/app.log"  # This will cause an error
)

# TODO 2: Fix memory leak simulation
# Problem: This will cause the container to eventually run out of memory
# HINT: Use a more controlled data structure with size limits
memory_hog = []

# TODO 3: Fix race condition with a shared counter
# Problem: Counter is accessed without proper synchronization
# HINT: Initialize and use a threading lock
counter = 0
counter_lock = None  # Should be a threading.Lock() but it's not initialized

# TODO 4: Fix port conflict
# Problem: Dockerfile exposes 5000, but the app runs on 8080
# HINT: Make the port consistent between Dockerfile and app code
PORT = 8080  # Dockerfile exposes 5000, but the app runs on 8080

# TODO 5: Fix unreachable endpoint
# Problem: Health endpoint has an unnecessary complex path
# HINT: Simplify the path for easier access and testing
@app.route('/api/v1/health')  # Should be just /health for simplicity
def health():
    return jsonify({"status": "healthy"})

@app.route('/')
def home():
    global counter
    # TODO 6: Fix thread safety issue
    # Problem: Counter is incremented without lock protection
    # HINT: Use the counter_lock for thread-safe operations
    counter += 1
    return f"Welcome to the Debug App! Counter: {counter}"

# TODO 7: Fix memory leak endpoint
# Problem: This endpoint adds data to memory without limits
# HINT: Implement a bounded cache or circular buffer
@app.route('/memory-leak')
def memory_leak():
    global memory_hog
    # Adding 1MB of data on each request
    memory_hog.append('x' * 1024 * 1024)
    return jsonify({"message": "Added 1MB to memory", "total_leaks": len(memory_hog)})

# TODO 8: Fix error handling in unstable endpoint
# Problem: This endpoint sometimes crashes without proper error handling
# HINT: Implement try/except and return appropriate error responses
@app.route('/unstable')
def unstable():
    if random.randint(1, 3) == 1:
        # Simulate a crash
        raise Exception("Random crash occurred!")
    return jsonify({"message": "Lucky! No crash this time."})

# TODO 9: Fix blocking operation
# Problem: This endpoint blocks the entire server
# HINT: Use asynchronous processing or background threads
@app.route('/slow')
def slow():
    # Blocking sleep - this will block the entire server
    time.sleep(10)
    return jsonify({"message": "Finally responded after 10 seconds"})

# TODO 10: Fix environment variable handling
# Problem: Missing environment variable causes the app to crash
# HINT: Use .get() with a default value instead of direct access
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