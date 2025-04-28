from flask import Flask, jsonify
import os
import sys
import uuid
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

# Create a directory for temporary files
if not os.path.exists('./data'):
    os.makedirs('./data')

@app.route('/')
def home():
    return "Welcome to the Layers Demo App! Use /status for health check and /info for server information."

@app.route('/status')
def status():
    # Generate a random plot to simulate a processing workload
    plt.figure(figsize=(10, 6))
    data = np.random.randn(1000)
    plt.hist(data, bins=30)
    
    # Save the plot (this is to demonstrate file operations)
    filename = f"./data/plot-{uuid.uuid4()}.png"
    plt.savefig(filename)
    plt.close()
    
    # Create a dataframe (to demonstrate pandas usage)
    df = pd.DataFrame({
        'data': data, 
        'abs_value': np.abs(data),
        'squared': data ** 2
    })
    
    # Save to CSV (more file operations for demo)
    csv_file = f"./data/data-{uuid.uuid4()}.csv"
    df.to_csv(csv_file)
    
    # Return status info
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "files_created": [filename, csv_file],
        "python_version": sys.version
    })

@app.route('/info')
def info():
    return jsonify({
        "app": "layers-demo",
        "versions": {
            "python": sys.version,
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "matplotlib": plt.__version__
        },
        "env": {k: v for k, v in os.environ.items() if not k.startswith('_')}
    })

if __name__ == '__main__':
    print("Starting Layers Demo App...")
    app.run(host='0.0.0.0', port=5000, debug=False) 