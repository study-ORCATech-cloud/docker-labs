import os
import json
from flask import Flask, jsonify
from flask_restful import Api, Resource
import pymongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# MongoDB connection
mongo_host = os.getenv('MONGO_HOST', 'db-service')
mongo_port = int(os.getenv('MONGO_PORT', 27017))
mongo_user = os.getenv('MONGO_USER', '')
mongo_password = os.getenv('MONGO_PASSWORD', '')
mongo_db = os.getenv('MONGO_DB', 'apidb')

# Set up MongoDB client
try:
    if mongo_user and mongo_password:
        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}"
    else:
        mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"
    
    client = pymongo.MongoClient(mongo_uri)
    db = client[mongo_db]
    items_collection = db.items
    
    # Insert some sample data if collection is empty
    if items_collection.count_documents({}) == 0:
        sample_items = [
            {"name": "Item 1", "description": "Description for Item 1", "price": 10.99},
            {"name": "Item 2", "description": "Description for Item 2", "price": 20.49},
            {"name": "Item 3", "description": "Description for Item 3", "price": 5.99}
        ]
        items_collection.insert_many(sample_items)
    
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    # Still allow the app to run without database
    db = None
    items_collection = None

# API Resources
class Items(Resource):
    def get(self):
        if items_collection:
            items = list(items_collection.find({}, {"_id": 0}))
            return jsonify({"items": items})
        else:
            # Return sample data if no DB connection
            return jsonify({
                "items": [
                    {"name": "Sample Item 1", "description": "Sample Description 1", "price": 9.99},
                    {"name": "Sample Item 2", "description": "Sample Description 2", "price": 19.99}
                ],
                "note": "Using sample data - no database connection"
            })

class HealthCheck(Resource):
    def get(self):
        return {"status": "healthy", "service": "api-service"}

# Register API resources
api.add_resource(Items, '/api/items')
api.add_resource(HealthCheck, '/health')

# Root endpoint for API documentation
@app.route('/')
def index():
    return jsonify({
        "service": "API Service",
        "version": "1.0",
        "endpoints": [
            {"path": "/api/items", "method": "GET", "description": "Get all items"},
            {"path": "/health", "method": "GET", "description": "Service health check"}
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug) 