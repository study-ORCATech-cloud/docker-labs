from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATA_DIR = '/app/data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/write', methods=['POST'])
def write_data():
    content = request.json.get('content')
    with open(os.path.join(DATA_DIR, 'message.txt'), 'w') as f:
        f.write(content)
    return jsonify({'status': 'written', 'content': content})

@app.route('/read')
def read_data():
    try:
        with open(os.path.join(DATA_DIR, 'message.txt'), 'r') as f:
            content = f.read()
        return jsonify({'status': 'read', 'content': content})
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'No data found'}), 404

@app.route('/')
def home():
    return '''
    <h1>Docker Volumes Demo</h1>
    <p>This application demonstrates data persistence with Docker volumes.</p>
    <h2>Available endpoints:</h2>
    <ul>
        <li><code>POST /write</code> - Write data to a file in the volume</li>
        <li><code>GET /read</code> - Read data from the file in the volume</li>
    </ul>
    '''

if __name__ == '__main__':
    print("Starting Flask application...")
    print(f"Data directory: {DATA_DIR}")
    print("This app will store and retrieve data from this directory.")
    app.run(host='0.0.0.0', port=5000) 