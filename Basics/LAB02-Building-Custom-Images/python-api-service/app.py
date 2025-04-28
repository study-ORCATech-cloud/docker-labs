import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request

# Configure logging based on environment variable
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('api-service')

# Initialize Flask application
app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.environ.get('API_KEY', 'default-key')

# TODO: Add a debug mode configuration based on an environment variable
# HINT: Create a new environment variable called DEBUG_MODE and use it to
# enable/disable debug features in the application


@app.route('/health')
def health():
    """Health check endpoint for monitoring and liveness probes"""
    logger.info("Health check requested")
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@app.route('/api/data')
def get_data():
    """Secure API endpoint that requires API key authentication"""
    # Check for API key in header
    auth_key = request.headers.get('X-API-KEY')
    
    if auth_key != API_KEY:
        logger.warning(f"Unauthorized API access attempt from {request.remote_addr}")
        return jsonify({"error": "Unauthorized access"}), 401
    
    logger.info(f"Data requested by authorized client from {request.remote_addr}")
    
    # Return sample data
    data = {
        "message": "Hello from the containerized API!",
        "timestamp": datetime.now().isoformat(),
        "environment": os.environ.get('ENVIRONMENT', 'development')
    }
    
    return jsonify(data)


@app.route('/api/echo', methods=['POST'])
def echo():
    """Echo endpoint that returns the posted JSON data"""
    data = request.get_json()
    logger.debug(f"Echo request received with data: {data}")
    return jsonify(data)


# TODO: Implement a new security feature for the API
# HINT: Add a rate limiting feature to prevent abuse, or implement
# additional authentication methods. Create a new endpoint or middleware to demonstrate it.


if __name__ == '__main__':
    logger.info("Starting API service...")
    app.run(host='0.0.0.0', port=8000) 