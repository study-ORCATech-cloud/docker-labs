#!/usr/bin/env python3

import os
import socket
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # Log request
        print(f"Received request from {self.client_address[0]}")
        
        # Get hostname
        hostname = socket.gethostname()
        
        # Create response
        response = f"Hello from Python container!\n"
        response += f"Hostname: {hostname}\n"
        response += f"Time: {datetime.now().isoformat()}\n"
        
        self.wfile.write(response.encode())

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    # Use PORT environment variable if set, default to 8080
    port = int(os.environ.get("PORT", 8080))
    run_server(port) 