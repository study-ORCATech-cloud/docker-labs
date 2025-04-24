# LAB05-Debugging: Solutions

**INSTRUCTOR NOTE: This file contains complete solutions and should NOT be shared with students. It is for instructor reference only. Students should work through the exercises themselves without seeing these solutions in advance.**

This file contains solutions to the debugging exercises in LAB05-Debugging.

## Fixed Dockerfile

Here is a properly fixed Dockerfile addressing all the TODOs:

```dockerfile
FROM python:3.9-slim

# TODO 1: Set up a working directory
WORKDIR /app

# TODO 2: Install dependencies efficiently
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO 3: Fix file copying
COPY app.py .

# TODO 4: Fix port configuration
EXPOSE 5000

# TODO 8: Create log directory
RUN mkdir -p /app/logs && chmod 777 /app/logs

# TODO 7: Set environment variables
ENV PYTHONUNBUFFERED=1 \
    API_KEY=demo-key \
    FLASK_APP=app.py

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# TODO 6: Add healthcheck
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# TODO 5: Fix app execution path
CMD ["python", "/app/app.py"]
```

## Fixed app.py

Here is a fixed app.py addressing all the TODOs:

```python
from flask import Flask, jsonify, request
import os
import time
import random
import threading
import logging

app = Flask(__name__)

# TODO 1: Fix logging configuration
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

# TODO 2: Fix memory leak simulation
# Using a controlled data structure with a size limit
memory_cache = {}
MAX_CACHE_SIZE = 10  # Limit the number of items

# TODO 3: Fix race condition with a shared counter
counter = 0
counter_lock = threading.Lock()  # Initialize the lock

# TODO 4: Fix port conflict
PORT = 5000  # Now matches EXPOSE in Dockerfile

# TODO 5: Fix unreachable endpoint
@app.route('/health')  # Simplified path
def health():
    return jsonify({"status": "healthy"})

@app.route('/')
def home():
    global counter
    # TODO 6: Fix thread safety issue
    with counter_lock:  # Using lock for thread safety
        counter += 1
    return f"Welcome to the Debug App! Counter: {counter}"

# TODO 7: Fix memory leak endpoint
@app.route('/memory')
def memory():
    global memory_cache
    # Using a bounded cache
    key = str(time.time())
    
    # Remove oldest item if at capacity
    if len(memory_cache) >= MAX_CACHE_SIZE:
        oldest_key = min(memory_cache.keys())
        del memory_cache[oldest_key]
    
    # Add limited size item
    memory_cache[key] = 'x' * 1024  # Just 1KB instead of 1MB
    
    return jsonify({
        "message": "Added item to memory cache", 
        "total_items": len(memory_cache)
    })

# TODO 8: Fix error handling in unstable endpoint
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

# TODO 9: Fix blocking operation
@app.route('/slow')
def async_operation():
    # Non-blocking - using a background thread
    threading.Thread(target=background_task).start()
    return jsonify({"message": "Operation started in background"})

def background_task():
    logger.info("Starting background operation")
    time.sleep(10)  # This won't block the server
    logger.info("Background operation completed")

# TODO 10: Fix environment variable handling
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
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in echo endpoint: {str(e)}")
        return jsonify({"error": "An error occurred processing the request"}), 500

if __name__ == '__main__':
    logger.info(f"Starting Flask app on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
```

## Detailed Explanations of Fixes

### Dockerfile Fixes

1. **Working Directory**: Added WORKDIR to set up /app as the working directory
2. **Dependency Installation**: Used requirements.txt with a single pip command
3. **File Copying**: Fixed file path to copy to the working directory
4. **Port Configuration**: Kept port 5000 but fixed app.py to match
5. **Execution Path**: Used absolute path to ensure app.py can be found
6. **Healthcheck**: Added healthcheck that calls the /health endpoint
7. **Environment Variables**: Set API_KEY and other necessary variables
8. **Log Directory**: Created the log directory with proper permissions

### Application Fixes

1. **Logging Configuration**: Changed log path to /app/logs and ensured the directory exists
2. **Memory Leak**: Replaced unbounded list with a dictionary with size limits
3. **Race Condition**: Initialized and used a proper threading lock
4. **Port Conflict**: Changed application port to match Dockerfile's exposed port
5. **Unreachable Endpoint**: Simplified the health endpoint path
6. **Thread Safety**: Used lock to protect counter increments
7. **Memory Leak Endpoint**: Implemented a bounded cache with cleanup logic
8. **Error Handling**: Added proper try/except blocks with informative responses
9. **Blocking Operation**: Used background thread for long-running operations
10. **Environment Variables**: Used os.environ.get() with default values

## Testing the Solutions

You can verify that the solutions work by:

1. Building and running the container:
   ```bash
   docker build -t debug-app:fixed .
   docker run -d -p 5000:5000 --name fixed-container debug-app:fixed
   ```

2. Testing the endpoints:
   ```bash
   curl http://localhost:5000/
   curl http://localhost:5000/health
   curl http://localhost:5000/config
   ```

3. Checking container health:
   ```bash
   docker inspect fixed-container | grep Health
   ```

4. Monitoring logs:
   ```bash
   docker logs fixed-container
   ```

The container should now be stable, handle errors gracefully, use resources efficiently, and pass its healthcheck. 