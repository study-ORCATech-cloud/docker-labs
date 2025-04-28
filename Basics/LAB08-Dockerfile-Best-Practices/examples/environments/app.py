#!/usr/bin/env python3

from flask import Flask, jsonify
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Environment configuration
ENV = os.environ.get('ENVIRONMENT', 'development')
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
API_KEY = os.environ.get('API_KEY', 'dev-key-123')
DB_HOST = os.environ.get('DB_HOST', 'localhost')

logger.info(f"Starting application in {ENV} environment")
if DEBUG:
    logger.warning("Debug mode is enabled. Not recommended for production!")

@app.route('/')
def index():
    logger.info("Serving index route")
    return jsonify({
        'message': f'Hello from {ENV} environment!',
        'environment': ENV,
        'debug': DEBUG,
        'database': DB_HOST
    })

@app.route('/config')
def config():
    # Note: In production, you should not expose sensitive configuration
    logger.debug("Serving config route")
    return jsonify({
        'environment': ENV,
        'debug': DEBUG,
        'db_host': DB_HOST,
        'api_key': API_KEY if ENV != 'production' else '***hidden***'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=DEBUG) 