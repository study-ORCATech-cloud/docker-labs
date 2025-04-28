#!/usr/bin/env python3
from flask import Flask, request, jsonify
import json
import os
import logging
import datetime

app = Flask(__name__)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Directory to store webhook data
DATA_DIR = 'webhook_data'
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/')
def index():
    """Simple index route to verify the service is running"""
    return jsonify({
        'status': 'online',
        'service': 'Docker Hub Webhook Receiver',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint to receive Docker Hub webhooks"""
    if not request.json:
        logger.warning("Received non-JSON payload")
        return jsonify({'status': 'error', 'message': 'Payload must be JSON'}), 400
    
    # Extract data from the webhook
    data = request.json
    logger.info(f"Received webhook: {json.dumps(data, indent=2)}")
    
    # Extract useful information
    try:
        push_data = data.get('push_data', {})
        repo_data = data.get('repository', {})
        
        pushed_at = push_data.get('pushed_at', '')
        pusher = push_data.get('pusher', 'unknown')
        tag = push_data.get('tag', 'latest')
        repo_name = repo_data.get('repo_name', 'unknown')
        
        logger.info(f"Image push: {repo_name}:{tag} by {pusher}")
        
        # Save webhook data to file for inspection
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{DATA_DIR}/webhook_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Saved webhook data to {filename}")
        
        # Example: Trigger different actions based on tags
        if tag == 'prod' or tag == 'production':
            logger.info("Production image detected - would trigger deployment here")
            # In a real scenario, you might call a deployment function:
            # deploy_to_production(repo_name, tag)
        elif tag == 'staging':
            logger.info("Staging image detected - would trigger staging deployment")
            # deploy_to_staging(repo_name, tag)
        elif tag == 'latest':
            logger.info("Latest tag updated - would trigger development environment update")
            # update_dev_environment(repo_name)
        
        # Always save the latest webhook for easy access
        with open(f"{DATA_DIR}/last_webhook.json", 'w') as f:
            json.dump(data, f, indent=2)
            
        return jsonify({
            'status': 'success',
            'message': f"Processed webhook for {repo_name}:{tag}",
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Error processing webhook: {str(e)}"
        }), 500

# Example of a separate function that could be triggered by webhooks
def send_notification(repo_name, tag, pusher):
    """Send a notification about the image push (stub)"""
    logger.info(f"NOTIFICATION: {pusher} pushed {repo_name}:{tag}")
    # In a real implementation, you might:
    # - Send an email notification
    # - Send a Slack message
    # - Update a status dashboard
    # - etc.

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Docker Hub webhook receiver on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True) 