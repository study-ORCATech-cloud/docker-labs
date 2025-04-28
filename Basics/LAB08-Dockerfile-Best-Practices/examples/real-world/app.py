#!/usr/bin/env python3

import os
import time
import logging
import json
from datetime import datetime
from flask import Flask, jsonify, request, render_template
import redis
import requests

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Environment configuration
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
API_KEY = os.environ.get('API_KEY', 'dev-key-123')
EXTERNAL_API_URL = os.environ.get('EXTERNAL_API_URL', 'https://jsonplaceholder.typicode.com')

# Redis configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

# Connect to Redis
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except redis.ConnectionError as e:
    logger.warning(f"Could not connect to Redis: {e}")
    redis_client = None

# Sample database (would be a real database in production)
products = [
    {"id": 1, "name": "Product 1", "price": 19.99, "category": "electronics"},
    {"id": 2, "name": "Product 2", "price": 29.99, "category": "clothing"},
    {"id": 3, "name": "Product 3", "price": 9.99, "category": "books"}
]

@app.route('/')
def index():
    logger.info("Serving index page")
    return jsonify({
        "message": "Welcome to the Real-World API",
        "version": "1.0.0",
        "endpoints": [
            "/api/products",
            "/api/products/<id>",
            "/api/cache/stats",
            "/api/external/users",
            "/health"
        ]
    })

@app.route('/health')
def health():
    redis_status = "UP" if redis_client and redis_client.ping() else "DOWN"
    
    try:
        external_status = "UP" if requests.get(f"{EXTERNAL_API_URL}/posts/1").status_code == 200 else "DOWN"
    except requests.RequestException:
        external_status = "DOWN"
    
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "redis": redis_status,
        "external_api": external_status
    }
    
    return jsonify(status)

@app.route('/api/products')
def get_products():
    category = request.args.get('category')
    
    if category:
        filtered_products = [p for p in products if p['category'] == category]
        return jsonify(filtered_products)
    
    return jsonify(products)

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    # Try to get from cache first
    if redis_client:
        cached_product = redis_client.get(f"product:{product_id}")
        if cached_product:
            logger.info(f"Cache hit for product:{product_id}")
            return jsonify(json.loads(cached_product))
    
    # If not in cache or no Redis, get from "database"
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    # Store in cache for next time
    if redis_client:
        redis_client.setex(
            f"product:{product_id}", 
            300,  # Cache for 5 minutes
            json.dumps(product)
        )
        logger.info(f"Cached product:{product_id}")
    
    return jsonify(product)

@app.route('/api/cache/stats')
def cache_stats():
    if not redis_client:
        return jsonify({"error": "Redis not connected"}), 503
    
    info = redis_client.info()
    return jsonify({
        "used_memory": info.get('used_memory_human', 'unknown'),
        "connected_clients": info.get('connected_clients', 0),
        "uptime": info.get('uptime_in_seconds', 0)
    })

@app.route('/api/external/users')
def external_users():
    # Implement caching for external API calls
    cache_key = "external:users"
    
    if redis_client:
        cached_users = redis_client.get(cache_key)
        if cached_users:
            logger.info("Cache hit for external users")
            return jsonify(json.loads(cached_users))
    
    try:
        response = requests.get(f"{EXTERNAL_API_URL}/users", timeout=5)
        response.raise_for_status()
        users = response.json()
        
        # Cache the result
        if redis_client:
            redis_client.setex(cache_key, 600, json.dumps(users))  # Cache for 10 minutes
            
        return jsonify(users)
    except requests.RequestException as e:
        logger.error(f"Error fetching external API: {e}")
        return jsonify({"error": "Could not fetch external API data"}), 503

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=DEBUG) 