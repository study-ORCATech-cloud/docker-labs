import os
import socket
from flask import Flask, jsonify
import pymongo
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# MongoDB connection
mongo_host = os.environ.get('MONGO_HOST', 'db')
mongo_port = int(os.environ.get('MONGO_PORT', 27017))
mongo_db = os.environ.get('MONGO_DB', 'networkdemo')

# Sample data to return when DB is not available
sample_data = [
    "Item 1 (Sample data - DB not connected)",
    "Item 2 (Sample data - DB not connected)",
    "Item 3 (Sample data - DB not connected)"
]

# Test DB connection
db_client = None
db_connected = False

try:
    # Try to connect to MongoDB
    db_client = pymongo.MongoClient(f"mongodb://{mongo_host}:{mongo_port}/", serverSelectionTimeoutMS=2000)
    db_client.server_info()  # Will throw an exception if not connected
    db = db_client[mongo_db]
    
    # Check if collection exists, if not create and populate
    if 'items' not in db.list_collection_names():
        items_collection = db.items
        items_collection.insert_many([
            {"name": "Item 1 (From DB)", "description": "This is item 1"},
            {"name": "Item 2 (From DB)", "description": "This is item 2"},
            {"name": "Item 3 (From DB)", "description": "This is item 3"}
        ])
    
    db_connected = True
    print("Successfully connected to MongoDB")
    
except (ConnectionFailure, pymongo.errors.ServerSelectionTimeoutError) as e:
    print(f"Failed to connect to MongoDB: {e}")
    db_connected = False

@app.route('/data')
def get_data():
    # Get data from MongoDB if connected, otherwise return sample data
    if db_connected:
        try:
            items = list(db.items.find({}, {"_id": 0, "name": 1}))
            return jsonify({
                "data": [item["name"] for item in items],
                "source": "database"
            })
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return jsonify({
                "data": sample_data,
                "source": "sample (error retrieving from db)",
                "error": str(e)
            })
    else:
        return jsonify({
            "data": sample_data,
            "source": "sample (db not connected)"
        })

@app.route('/health')
def health():
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    # Check DB connectivity
    db_status = "Connected" if db_connected else "Not connected"
    
    return jsonify({
        "status": "healthy",
        "hostname": hostname,
        "ip": container_ip,
        "database": {
            "host": mongo_host,
            "port": mongo_port,
            "status": db_status
        }
    })

@app.route('/network-info')
def network_info():
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    # Check connectivity to other services
    frontend_reachable = False
    frontend_ip = "Unknown"
    db_reachable = False
    db_ip = "Unknown"
    
    try:
        frontend_ip = socket.gethostbyname('frontend')
        frontend_reachable = True
    except socket.gaierror:
        pass
    
    try:
        db_ip = socket.gethostbyname(mongo_host)
        
        # More detailed check for DB
        if db_connected:
            db_reachable = True
        else:
            # We can resolve but not connect
            db_reachable = False
    except socket.gaierror:
        pass
    
    # Get all network interfaces
    import netifaces
    interfaces = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            interfaces[iface] = addrs[netifaces.AF_INET][0]['addr']
    
    return jsonify({
        "container": {
            "service": "backend",
            "hostname": hostname,
            "ip": container_ip,
            "interfaces": interfaces
        },
        "connections": {
            "frontend": {
                "hostname": "frontend",
                "ip": frontend_ip,
                "reachable": frontend_reachable
            },
            "db": {
                "hostname": mongo_host,
                "ip": db_ip,
                "reachable": db_reachable,
                "connected": db_connected
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 