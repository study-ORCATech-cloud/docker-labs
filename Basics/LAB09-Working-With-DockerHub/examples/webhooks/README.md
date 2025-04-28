# Working with Docker Hub Webhooks

This directory contains examples and instructions for configuring and using Docker Hub webhooks.

## What are Docker Hub Webhooks?

Webhooks allow you to trigger automated actions whenever an image is pushed to your Docker Hub repository. They send HTTP POST requests to a specified URL with information about the push event.

## How Webhooks Work

1. You configure a webhook in your Docker Hub repository, specifying a target URL
2. When an image is pushed to the repository, Docker Hub sends a POST request to that URL
3. Your server receives the webhook data and performs actions based on the event

## Setting Up a Webhook Receiver

This directory includes a simple Python webhook receiver application:

- `webhook_receiver.py`: A Flask application that receives and processes webhooks
- `requirements.txt`: Python dependencies
- `Dockerfile`: For containerizing the webhook receiver

### Running the Webhook Receiver

```bash
# Install dependencies
pip install -r requirements.txt

# Run the receiver
python webhook_receiver.py
```

The receiver will listen on port 5000 by default. For public internet access, you'll need to either:
- Deploy to a cloud provider
- Use a tunnel service like ngrok for local testing

### Using ngrok for Local Testing

```bash
# Install ngrok
# Start a tunnel to your local webhook receiver
ngrok http 5000

# Use the URL provided by ngrok (e.g., https://abc123.ngrok.io/webhook) in your Docker Hub webhook configuration
```

## Configuring a Webhook in Docker Hub

1. Log in to Docker Hub
2. Navigate to your repository
3. Click on "Webhooks" in the left sidebar
4. Click "Create Webhook"
5. Enter a name for the webhook (e.g., "Deployment Trigger")
6. Enter the webhook URL (e.g., https://your-server.com/webhook or your ngrok URL)
7. Click "Create"

## Webhook Payload Structure

When an image is pushed, Docker Hub sends a JSON payload similar to:

```json
{
  "callback_url": "https://registry.hub.docker.com/...",
  "push_data": {
    "pushed_at": 1562136071,
    "pusher": "username",
    "tag": "latest"
  },
  "repository": {
    "comment_count": 0,
    "date_created": 1562135973,
    "description": "",
    "dockerfile": "#...",
    "full_description": "",
    "is_official": false,
    "is_private": false,
    "is_trusted": false,
    "name": "repository",
    "namespace": "username",
    "owner": "username",
    "repo_name": "username/repository",
    "repo_url": "https://hub.docker.com/r/username/repository",
    "star_count": 0,
    "status": "Active"
  }
}
```

## Common Webhook Use Cases

- **Continuous Deployment**: Automatically deploy updated images to your infrastructure
- **Notifications**: Send alerts to Slack, email, or other communication tools
- **Testing**: Trigger automated tests against new image versions
- **Documentation**: Update documentation when new image versions are released
- **Image Scanning**: Trigger security scans of new images

## TODO

Complete the following tasks:
1. Create a simple webhook receiver using the provided Python application
2. Configure a webhook in your Docker Hub repository
3. Test the webhook with image pushes
4. Document the webhook payload and potential use cases
5. Implement a basic automation triggered by the webhook (such as a notification or deployment)
6. Create a file called `webhook_notes.md` with your observations and experiences 