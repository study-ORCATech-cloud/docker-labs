from flask import Flask, jsonify, request
import os
import time
import random
import threading
import logging

app = Flask(__name__)

# Configure logging properly
log_dir = "/app/logs"  # Using a directory that exists (created in Dockerfile)
os.makedirs(log_dir, exist_ok=True)  # Make sure directory exists
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/app.log"),
        logging.StreamHandler()  # Also log to stdout/stderr for Docker logs
    ]
)
logger = logging.getLogger(__name__)

# Fixed: Using a controlled data structure 
memory_cache = {}

# Fixed: Proper thread synchronization
counter = 0
counter_lock = threading.Lock()

# Fixed: Using the correct port that matches the Dockerfile
PORT = 5000  # Matches EXPOSE in Dockerfile

# Fixed: Simplified endpoint path
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/')
def home():
    global counter
    # Fixed: Using lock for counter increments
    with counter_lock:
        counter += 1
    return f"Welcome to the Debug App! Counter: {counter}"

# Fixed: Controlled memory usage with size limit
@app.route('/memory')
def memory():
    key = str(time.time())
    # Only keep last 10 items
    if len(memory_cache) >= 10:
        # Remove oldest item
        oldest_key = min(memory_cache.keys())
        del memory_cache[oldest_key]
    
    # Add new item - limited size
    memory_cache[key] = 'x' * 1024  # Just 1KB
    
    return jsonify({
        "message": "Added item to memory cache", 
        "total_items": len(memory_cache)
    })

# Fixed: Proper error handling
@app.route('/unstable')
def unstable():
    try:
        if random.randint(1, 3) == 1:
            logger.warning("Simulating an error but handling it properly")
            return jsonify({"message": "Detected and handled a potential error"}), 500
        return jsonify({"message": "Operation completed successfully"})
    except Exception as e:
        logger.error(f"Error in unstable endpoint: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

# Fixed: Using non-blocking operation
@app.route('/async')
def async_operation():
    # Non-blocking - just a message that it would be run in background
    threading.Thread(target=background_operation).start()
    return jsonify({"message": "Operation started in background"})

def background_operation():
    logger.info("Starting background operation")
    time.sleep(10)  # This won't block the server
    logger.info("Background operation completed")

# Fixed: Environment variable with default
@app.route('/config')
def config():
    # Using .get() with a default value
    api_key = os.environ.get('API_KEY', 'default-key-for-development')
    return jsonify({"api_key": api_key})

@app.route('/working')
def working():
    return jsonify({"message": "This endpoint works properly!"})

@app.route('/echo', methods=['POST'])
def echo():
    try:
        data = request.get_json()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in echo endpoint: {str(e)}")
        return jsonify({"error": "Invalid JSON data"}), 400

if __name__ == '__main__':
    logger.info(f"Starting Flask app on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True) 