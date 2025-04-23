import os
import socket
from flask import Flask, jsonify, request
import pymongo
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from bson.json_util import dumps
import json

app = Flask(__name__)

# MongoDB connection
mongo_host = os.environ.get('MONGO_HOST', 'db-service')
mongo_port = int(os.environ.get('MONGO_PORT', 27017))
mongo_db = os.environ.get('MONGO_DB', 'microservices')
mongo_user = os.environ.get('MONGO_USER', '')
mongo_password = os.environ.get('MONGO_PASSWORD', '')

# Sample data when DB is not available
sample_users = [
    {"_id": "1", "name": "John Doe", "email": "john@example.com", "role": "admin"},
    {"_id": "2", "name": "Jane Smith", "email": "jane@example.com", "role": "user"},
    {"_id": "3", "name": "Bob Johnson", "email": "bob@example.com", "role": "user"}
]

# Connect to MongoDB
db_client = None
db_connected = False
users_collection = None

try:
    # Build connection string
    if mongo_user and mongo_password:
        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}"
    else:
        mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"
    
    # Connect with timeout
    db_client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
    db_client.server_info()  # Will throw an exception if not connected
    db = db_client[mongo_db]
    users_collection = db.users
    
    # Create index on email field
    users_collection.create_index("email", unique=True)
    
    # Insert sample data if collection is empty
    if users_collection.count_documents({}) == 0:
        users_collection.insert_many([
            {"name": "John Doe", "email": "john@example.com", "role": "admin"},
            {"name": "Jane Smith", "email": "jane@example.com", "role": "user"},
            {"name": "Bob Johnson", "email": "bob@example.com", "role": "user"}
        ])
    
    db_connected = True
    print("Successfully connected to MongoDB")
    
except (ConnectionFailure, pymongo.errors.ServerSelectionTimeoutError) as e:
    print(f"Failed to connect to MongoDB: {e}")
    db_connected = False

@app.route('/')
def index():
    """Root endpoint"""
    hostname = socket.gethostname()
    return jsonify({
        "service": "Users Service",
        "hostname": hostname,
        "database": {
            "connected": db_connected,
            "host": mongo_host
        },
        "endpoints": [
            {"path": "/users", "method": "GET", "description": "Get all users"},
            {"path": "/users/<id>", "method": "GET", "description": "Get user by ID"},
            {"path": "/users", "method": "POST", "description": "Create a new user"},
            {"path": "/health", "method": "GET", "description": "Service health check"}
        ]
    })

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    if db_connected:
        try:
            users = list(users_collection.find())
            return Response(dumps(users), mimetype='application/json')
        except Exception as e:
            return jsonify({"error": str(e), "users": sample_users})
    else:
        return jsonify({"users": sample_users, "note": "Using sample data - DB not connected"})

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    if db_connected:
        try:
            # Try to convert to ObjectId for MongoDB query
            try:
                user_obj_id = ObjectId(user_id)
                user = users_collection.find_one({"_id": user_obj_id})
            except:
                # If not a valid ObjectId, try as a string
                user = users_collection.find_one({"_id": user_id})
            
            if user:
                return Response(dumps(user), mimetype='application/json')
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Use sample data
        user = next((u for u in sample_users if u["_id"] == user_id), None)
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    if not request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    user_data = request.json
    
    if db_connected:
        try:
            # Check required fields
            if not all(k in user_data for k in ("name", "email")):
                return jsonify({"error": "Missing required fields"}), 400
            
            result = users_collection.insert_one(user_data)
            
            if result.inserted_id:
                return jsonify({
                    "success": True,
                    "user_id": str(result.inserted_id)
                }), 201
            else:
                return jsonify({"error": "Failed to create user"}), 500
        except pymongo.errors.DuplicateKeyError:
            return jsonify({"error": "Email already exists"}), 409
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Simulate creation with sample data
        return jsonify({
            "success": True,
            "user_id": "sample_" + str(len(sample_users) + 1),
            "note": "Using sample data - DB not connected"
        }), 201

# Helper for JSON serialization of ObjectId
class Response(Flask.response_class):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, str):
            response = response.encode('utf-8')
        return super(Response, cls).force_type(response, environ)

@app.route('/network-info')
def network_info():
    """Get network information"""
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    # Check DB connectivity
    db_ip = None
    db_reachable = False
    
    try:
        db_ip = socket.gethostbyname(mongo_host)
        db_reachable = db_connected
    except socket.gaierror:
        pass
    
    # Get network interfaces
    import netifaces
    interfaces = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            interfaces[iface] = addrs[netifaces.AF_INET][0]['addr']
    
    return jsonify({
        "service": "users-service",
        "hostname": hostname,
        "ip": container_ip,
        "interfaces": interfaces,
        "connectivity": {
            "database": {
                "host": mongo_host,
                "ip": db_ip,
                "reachable": db_reachable,
                "connected": db_connected
            }
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    hostname = socket.gethostname()
    return jsonify({
        "status": "healthy",
        "service": "users-service",
        "hostname": hostname,
        "database": {
            "connected": db_connected
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 