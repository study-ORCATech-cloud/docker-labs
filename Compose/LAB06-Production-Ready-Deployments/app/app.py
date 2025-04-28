from flask import Flask, render_template, jsonify
import redis
import os
import socket
import logging
from logging.handlers import RotatingFileHandler
import time

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')
    
handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=3)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Initialize Flask app
app = Flask(__name__)

# Get environment variables or set defaults
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
APP_ENV = os.environ.get('APP_ENV', 'development')

# Graceful connection handling with Redis
def get_redis_client():
    try:
        if REDIS_PASSWORD:
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                decode_responses=True
            )
        else:
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                decode_responses=True
            )
        return client
    except redis.ConnectionError as e:
        logger.error(f"Redis connection error: {e}")
        return None

@app.route('/')
def index():
    try:
        redis_client = get_redis_client()
        if redis_client:
            # Increment page view counter
            counter = redis_client.incr('hits')
            logger.info(f"Page viewed {counter} times")
        else:
            counter = "Redis connection failed"
            logger.warning("Redis connection failed on page view")
        
        hostname = socket.gethostname()
        return render_template('index.html', hostname=hostname, counter=counter, environment=APP_ENV)
    except Exception as e:
        logger.error(f"Error on index page: {e}")
        return "An error occurred", 500

@app.route('/health')
def health():
    try:
        # Check Redis connection
        redis_client = get_redis_client()
        if redis_client and redis_client.ping():
            redis_status = "healthy"
        else:
            redis_status = "unhealthy"
            
        health_data = {
            "status": "healthy" if redis_status == "healthy" else "degraded",
            "timestamp": time.time(),
            "components": {
                "redis": redis_status,
                "app": "healthy"
            },
            "environment": APP_ENV
        }
        
        status_code = 200 if health_data["status"] == "healthy" else 503
        return jsonify(health_data), status_code
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

# Resource usage endpoint (for demo purposes)
@app.route('/metrics')
def metrics():
    import psutil
    
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    metrics_data = {
        "cpu": {
            "percent": psutil.cpu_percent(interval=1)
        },
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent
        },
        "disk": {
            "total": disk.total,
            "free": disk.free,
            "percent": disk.percent
        }
    }
    
    return jsonify(metrics_data)

if __name__ == '__main__':
    # In production, we'll use gunicorn instead of the built-in server
    # This is just for development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=APP_ENV == 'development') 