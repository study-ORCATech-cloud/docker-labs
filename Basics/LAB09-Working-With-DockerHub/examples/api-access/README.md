# Working with Docker Hub API

This directory contains examples and instructions for interacting with the Docker Hub API programmatically.

## What is the Docker Hub API?

The Docker Hub API allows you to interact with Docker Hub programmatically, enabling:
- Repository management
- Image and tag manipulation
- Webhook configuration
- Access control management
- Automation of Docker Hub operations

## Prerequisites

Before using the Docker Hub API:
1. You need a Docker Hub account
2. You need to create an access token with appropriate permissions
3. Basic understanding of RESTful APIs and HTTP requests

## Creating an Access Token

1. Log in to Docker Hub
2. Go to Account Settings > Security
3. Click "New Access Token"
4. Enter a description for the token (e.g., "API Access")
5. Select the appropriate permissions:
   - Read Repository (for viewing repositories)
   - Write Repository (for managing repositories)
   - Delete Repository (for deleting repositories)
6. Click "Generate" and copy the token immediately (it won't be shown again)

## Docker Hub API Endpoints

The Docker Hub API is available at `https://hub.docker.com/v2/`.

Common endpoints include:
- `/repositories/{namespace}/`: List repositories
- `/repositories/{namespace}/{repository}/`: Repository details
- `/repositories/{namespace}/{repository}/tags/`: List tags
- `/repositories/{namespace}/{repository}/webhooks/`: Manage webhooks

## Sample Python Script

This directory contains a Python script `dockerhub_api.py` that demonstrates how to interact with the Docker Hub API:

```python
import requests
import os
import json

# Configuration
DOCKER_HUB_USERNAME = os.environ.get('DOCKER_HUB_USERNAME')
DOCKER_HUB_TOKEN = os.environ.get('DOCKER_HUB_TOKEN')

# Base API URL
API_URL = "https://hub.docker.com/v2"

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DOCKER_HUB_TOKEN}"
}

# Function to call the API and handle errors
def call_api(method, endpoint, data=None):
    url = f"{API_URL}{endpoint}"
    
    if method.lower() == 'get':
        response = requests.get(url, headers=headers)
    elif method.lower() == 'post':
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method.lower() == 'delete':
        response = requests.delete(url, headers=headers)
    elif method.lower() == 'patch':
        response = requests.patch(url, headers=headers, data=json.dumps(data))
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    if response.status_code >= 400:
        print(f"API Error: {response.status_code}")
        print(response.text)
        return None
        
    return response.json() if response.text else {}

# Various API operations
def list_repositories():
    """List all repositories for the user"""
    return call_api('get', f"/repositories/{DOCKER_HUB_USERNAME}/")

def get_repository_details(repository_name):
    """Get details for a specific repository"""
    return call_api('get', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}")

def list_tags(repository_name):
    """List all tags for a repository"""
    return call_api('get', f"/repositories/{DOCKER_HUB_USERNAME}/{repository_name}/tags")

def create_repository(repository_name, is_private=False):
    """Create a new repository"""
    data = {
        "namespace": DOCKER_HUB_USERNAME,
        "name": repository_name,
        "is_private": is_private,
        "description": f"Repository created via API for {repository_name}"
    }
    
    return call_api('post', "/repositories/", data)
```

## Using the Sample Script

To use the script:
1. Install the requirements: `pip install -r requirements.txt`
2. Set environment variables:
   ```
   export DOCKER_HUB_USERNAME="your-username"
   export DOCKER_HUB_TOKEN="your-token"
   ```
3. Run the script: `python dockerhub_api.py`

## Common API Operations

### Listing Your Repositories

```python
repositories = list_repositories()
print(f"Found {len(repositories['results'])} repositories:")
for repo in repositories['results']:
    print(f"- {repo['name']}")
```

### Creating a New Repository

```python
result = create_repository("my-new-repo", is_private=True)
if result:
    print(f"Repository created: {result['name']}")
```

### Getting Repository Details

```python
details = get_repository_details("my-repository")
print(f"Repository: {details['name']}")
print(f"Description: {details['description']}")
print(f"Stars: {details['star_count']}")
print(f"Pull Count: {details['pull_count']}")
```

### Listing Tags

```python
tags = list_tags("my-repository")
print(f"Tags for my-repository:")
for tag in tags['results']:
    print(f"- {tag['name']}")
```

## Automation Examples

This directory also includes examples of automating common Docker Hub tasks:

- `auto_cleanup.py`: Script to automatically delete old tags based on age or count
- `repo_backup.py`: Script to back up repository metadata and configurations
- `stats_collector.py`: Script to collect and report statistics on your repositories

## TODO

Complete the following tasks:
1. Generate a Docker Hub access token
2. Use the provided Python script to interact with the Docker Hub API
3. List your repositories programmatically
4. Get detailed information about a specific repository
5. Implement a simple script to automate repository management
6. Create a file called `api_notes.md` with your experiences and findings 