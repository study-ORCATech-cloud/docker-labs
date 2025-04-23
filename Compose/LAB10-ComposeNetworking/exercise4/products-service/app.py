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
sample_products = [
    {"_id": "1", "name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
    {"_id": "2", "name": "Office Chair", "price": 149.99, "category": "Furniture", "in_stock": True},
    {"_id": "3", "name": "Coffee Maker", "price": 89.99, "category": "Appliances", "in_stock": False}
]

# Connect to MongoDB
db_client = None
db_connected = False
products_collection = None

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
    products_collection = db.products
    
    # Create indexes
    products_collection.create_index("name")
    products_collection.create_index("category")
    
    # Insert sample data if collection is empty
    if products_collection.count_documents({}) == 0:
        products_collection.insert_many([
            {"name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
            {"name": "Office Chair", "price": 149.99, "category": "Furniture", "in_stock": True},
            {"name": "Coffee Maker", "price": 89.99, "category": "Appliances", "in_stock": False}
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
        "service": "Products Service",
        "hostname": hostname,
        "database": {
            "connected": db_connected,
            "host": mongo_host
        },
        "endpoints": [
            {"path": "/products", "method": "GET", "description": "Get all products"},
            {"path": "/products/<id>", "method": "GET", "description": "Get product by ID"},
            {"path": "/products", "method": "POST", "description": "Create a new product"},
            {"path": "/products/category/<category>", "method": "GET", "description": "Get products by category"},
            {"path": "/health", "method": "GET", "description": "Service health check"}
        ]
    })

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    if db_connected:
        try:
            products = list(products_collection.find())
            return Response(dumps(products), mimetype='application/json')
        except Exception as e:
            return jsonify({"error": str(e), "products": sample_products})
    else:
        return jsonify({"products": sample_products, "note": "Using sample data - DB not connected"})

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    if db_connected:
        try:
            # Try to convert to ObjectId for MongoDB query
            try:
                product_obj_id = ObjectId(product_id)
                product = products_collection.find_one({"_id": product_obj_id})
            except:
                # If not a valid ObjectId, try as a string
                product = products_collection.find_one({"_id": product_id})
            
            if product:
                return Response(dumps(product), mimetype='application/json')
            else:
                return jsonify({"error": "Product not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Use sample data
        product = next((p for p in sample_products if p["_id"] == product_id), None)
        if product:
            return jsonify(product)
        else:
            return jsonify({"error": "Product not found"}), 404

@app.route('/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category"""
    if db_connected:
        try:
            products = list(products_collection.find({"category": category}))
            if products:
                return Response(dumps(products), mimetype='application/json')
            else:
                return jsonify({"products": [], "message": "No products found in this category"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Use sample data
        filtered_products = [p for p in sample_products if p["category"].lower() == category.lower()]
        return jsonify({"products": filtered_products, "note": "Using sample data - DB not connected"})

@app.route('/products', methods=['POST'])
def create_product():
    """Create a new product"""
    if not request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    product_data = request.json
    
    if db_connected:
        try:
            # Check required fields
            if not all(k in product_data for k in ("name", "price", "category")):
                return jsonify({"error": "Missing required fields"}), 400
            
            # Set default for in_stock if not provided
            if "in_stock" not in product_data:
                product_data["in_stock"] = True
            
            result = products_collection.insert_one(product_data)
            
            if result.inserted_id:
                return jsonify({
                    "success": True,
                    "product_id": str(result.inserted_id)
                }), 201
            else:
                return jsonify({"error": "Failed to create product"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Simulate creation with sample data
        return jsonify({
            "success": True,
            "product_id": "sample_" + str(len(sample_products) + 1),
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
        
    # Try to connect to users-service
    users_service_host = 'users-service'
    users_service_reachable = False
    users_service_ip = None
    
    try:
        users_service_ip = socket.gethostbyname(users_service_host)
        users_service_reachable = True
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
        "service": "products-service",
        "hostname": hostname,
        "ip": container_ip,
        "interfaces": interfaces,
        "connectivity": {
            "database": {
                "host": mongo_host,
                "ip": db_ip,
                "reachable": db_reachable,
                "connected": db_connected
            },
            "users_service": {
                "host": users_service_host,
                "ip": users_service_ip,
                "reachable": users_service_reachable
            }
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    hostname = socket.gethostname()
    return jsonify({
        "status": "healthy",
        "service": "products-service",
        "hostname": hostname,
        "database": {
            "connected": db_connected
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 