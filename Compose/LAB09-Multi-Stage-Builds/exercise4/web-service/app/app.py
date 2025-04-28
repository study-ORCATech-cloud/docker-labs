import os
import requests
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# API Service configuration
api_host = os.getenv('API_HOST', 'api-service')
api_port = os.getenv('API_PORT', '5000')
api_url = f"http://{api_host}:{api_port}"

@app.route('/')
def index():
    try:
        # Fetch items from API
        response = requests.get(f"{api_url}/api/items", timeout=5)
        if response.status_code == 200:
            return render_template('index.html', items=response.json().get('items', []))
        else:
            error_message = f"API returned status code: {response.status_code}"
            return render_template('error.html', error=error_message)
    except requests.RequestException as e:
        return render_template('error.html', error=str(e))

@app.route('/api/status')
def api_status():
    try:
        # Check API health
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code == 200:
            return jsonify({
                "status": "connected",
                "api_status": response.json()
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"API returned status code: {response.status_code}"
            }), 500
    except requests.RequestException as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "web-service"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug) 