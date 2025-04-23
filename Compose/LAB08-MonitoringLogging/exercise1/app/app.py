#!/usr/bin/env python3
"""
Sample Flask application with Prometheus metrics
"""
import time
import random
from flask import Flask, request, jsonify, render_template_string
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest, REGISTRY, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter('app_request_count', 'Total number of requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint'])
IN_PROGRESS = Gauge('app_requests_in_progress', 'Number of requests in progress', ['method', 'endpoint'])
LAST_REQUEST_TIME = Gauge('app_last_request_timestamp', 'Timestamp of the last request')
CPU_LOAD = Gauge('app_simulated_cpu_load', 'Simulated CPU load')
RANDOM_COUNT = Summary('app_random_count', 'Random count that increases and decreases')

# Update simulated CPU load periodically (random walk)
def update_cpu_load():
    current = CPU_LOAD._value.get() or 0
    change = (random.random() - 0.5) * 0.1
    new_value = max(0, min(1, current + change))
    CPU_LOAD.set(new_value)

# Update random count
def update_random_count():
    value = random.randint(1, 100)
    RANDOM_COUNT.observe(value)

@app.before_request
def before_request():
    request.start_time = time.time()
    endpoint = request.endpoint or 'unknown'
    IN_PROGRESS.labels(request.method, endpoint).inc()

@app.after_request
def after_request(response):
    endpoint = request.endpoint or 'unknown'
    LAST_REQUEST_TIME.set(time.time())
    
    # Record request latency
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.method, endpoint).observe(latency)
    
    # Count requests by status and method
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    
    # Decrement gauge of in-progress requests
    IN_PROGRESS.labels(request.method, endpoint).dec()
    
    # Simulate metrics that change
    update_cpu_load()
    update_random_count()
    
    return response

@app.route('/')
def index():
    """Main page with metrics simulation"""
    # Simple HTML template with Bootstrap
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prometheus Metrics Demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { padding: 20px; }
            .metrics-panel { margin-top: 20px; }
            .card { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Prometheus Metrics Demo</h1>
            <p class="lead">This application exposes Prometheus metrics to demonstrate monitoring in Docker Compose.</p>
            
            <div class="row metrics-panel">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">Generate Traffic</div>
                        <div class="card-body">
                            <p>Click the buttons below to generate different types of traffic:</p>
                            <a href="/api/data" class="btn btn-primary mb-2">GET Request</a>
                            <a href="/api/slow" class="btn btn-warning mb-2">Slow Request</a>
                            <button onclick="postData()" class="btn btn-success mb-2">POST Request</button>
                            <a href="/error" class="btn btn-danger mb-2">Error Request</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">Prometheus Endpoints</div>
                        <div class="card-body">
                            <p>Access metrics at: <a href="/metrics">/metrics</a></p>
                            <p>View metrics in Prometheus: <a href="http://localhost:9090/graph" target="_blank">Prometheus UI</a></p>
                            <p>View dashboards in Grafana: <a href="http://localhost:3000/dashboards" target="_blank">Grafana</a></p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-info mt-4">
                <strong>Tip:</strong> Open the browser console to see responses from the API endpoints.
            </div>
        </div>
        
        <script>
            function postData() {
                fetch('/api/data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        data: 'test',
                        timestamp: new Date().toISOString()
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('POST response:', data);
                    alert('POST request sent! Check console for details.');
                });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    """API endpoint that returns mock data"""
    if request.method == 'POST':
        data = request.get_json() or {}
        return jsonify({"status": "success", "received": data})
    else:
        # Simulate some processing time
        time.sleep(random.random() * 0.1)
        return jsonify({
            "status": "success",
            "data": [random.randint(1, 100) for _ in range(5)],
            "timestamp": time.time()
        })

@app.route('/api/slow')
def api_slow():
    """Deliberately slow API endpoint"""
    # Simulate a slow response
    sleep_time = 1 + random.random()
    time.sleep(sleep_time)
    return jsonify({
        "status": "success",
        "data": "Slow response completed",
        "sleep_time": sleep_time
    })

@app.route('/error')
def error():
    """Endpoint that generates an error"""
    # Simulate an error
    if random.random() < 0.8:  # 80% chance of error
        return jsonify({"status": "error", "message": "Simulated error"}), 500
    else:
        return jsonify({"status": "error", "message": "Simulated client error"}), 400

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    # Set initial CPU load
    CPU_LOAD.set(random.random() * 0.5)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080) 