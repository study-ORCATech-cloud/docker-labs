# LAB09: Working With DockerHub - Solutions

This document provides solutions to the exercises in LAB09. **Only consult these solutions after attempting to solve the problems yourself.** The learning comes from working through the challenges, not just reading the answers.

## Task 1: Getting Started with Docker Hub

### Creating a Docker Hub Account

1. Navigate to [Docker Hub](https://hub.docker.com/)
2. Click on "Sign Up" and provide your email, username, and password
3. Verify your email by clicking the link sent to your email address
4. Log in to Docker Hub with your credentials

### Configuring Docker CLI for Docker Hub

To log in to Docker Hub from your terminal:

```bash
docker login
```

Enter your Docker Hub username and password when prompted. If successful, you'll see:

```
Login Succeeded
```

This creates a `~/.docker/config.json` file with your authentication credentials.

### Key Docker Hub Features

- **Repositories**: Public and private image storage
- **Tags**: Version control for images
- **README**: Documentation for your images
- **Description**: Short summary of the repository
- **Webhook**: Trigger actions on image updates
- **Automated builds**: Connect to Git repositories for CI/CD
- **Teams and Organizations**: Collaborative image management
- **Security scanning**: Vulnerability detection in images

## Task 2: Creating and Managing Repositories

### Creating a Public Repository

1. Log in to Docker Hub
2. Click "Create Repository" button
3. Enter a name (e.g., "my-python-app")
4. Leave the visibility as "Public"
5. Add a description (optional)
6. Click "Create"

### Creating a Private Repository

1. Log in to Docker Hub
2. Click "Create Repository" button
3. Enter a name (e.g., "my-private-app")
4. Set visibility to "Private"
5. Add a description (optional)
6. Click "Create"

### Repository Settings

- **General**: Name, description, and visibility
- **Collaborators**: Add users who can access private repositories
- **Webhooks**: Configure notifications on image updates
- **Build settings**: Configure automated builds
- **Tags**: Manage image versions
- **Settings**: Delete repository, change ownership

### Differences Between Public and Private Repositories

| Feature | Public | Private |
|---------|--------|---------|
| Visibility | Anyone can view and pull | Only you and collaborators |
| Cost | Free | Included in paid plans (or limited free) |
| Collaborators | Unlimited | Limited by plan |
| Pull limit | Subject to rate limits | Subject to rate limits |
| Use case | Open source, publicly shared apps | Proprietary software, internal tools |

## Task 3: Building and Pushing Images

### Building an Image

```bash
# Navigate to the directory with the Dockerfile
cd examples/pushing-images

# Build the image with a proper tag (username/repository:tag)
docker build -t yourusername/my-python-app:v1.0 .
```

### Tagging an Image

```bash
# If you've already built the image with another name
docker tag my-python-app:latest yourusername/my-python-app:v1.0

# Add additional tags (like 'latest')
docker tag yourusername/my-python-app:v1.0 yourusername/my-python-app:latest
```

### Pushing Images to Docker Hub

```bash
# Push the specific version
docker push yourusername/my-python-app:v1.0

# Push the latest tag
docker push yourusername/my-python-app:latest
```

### Verifying in Docker Hub

1. Log in to Docker Hub
2. Navigate to your repository
3. Click on "Tags" to see your pushed images
4. Check that tags and metadata are correct

### Updating and Pushing a New Version

```bash
# Make changes to your application code
# Rebuild with a new version tag
docker build -t yourusername/my-python-app:v1.1 .

# Push the new version
docker push yourusername/my-python-app:v1.1

# Update the latest tag
docker tag yourusername/my-python-app:v1.1 yourusername/my-python-app:latest
docker push yourusername/my-python-app:latest
```

## Task 4: Tagging and Versioning Strategies

### Semantic Versioning Implementation

```bash
# Major.Minor.Patch
docker build -t yourusername/versioned-app:1.0.0 .

# For a patch update (bug fixes)
docker build -t yourusername/versioned-app:1.0.1 .

# For a minor update (new features, backward compatible)
docker build -t yourusername/versioned-app:1.1.0 .

# For a major update (breaking changes)
docker build -t yourusername/versioned-app:2.0.0 .
```

### Multiple Tagged Versions

```bash
# Build once
docker build -t yourusername/multi-tag-app:3.2.1 .

# Create additional tags
docker tag yourusername/multi-tag-app:3.2.1 yourusername/multi-tag-app:3.2
docker tag yourusername/multi-tag-app:3.2.1 yourusername/multi-tag-app:3
docker tag yourusername/multi-tag-app:3.2.1 yourusername/multi-tag-app:latest

# Push all tags
docker push yourusername/multi-tag-app:3.2.1
docker push yourusername/multi-tag-app:3.2
docker push yourusername/multi-tag-app:3
docker push yourusername/multi-tag-app:latest
```

### Environment-specific Tags

```bash
# Build once
docker build -t yourusername/env-app:1.0.0 .

# Create environment-specific tags
docker tag yourusername/env-app:1.0.0 yourusername/env-app:dev
docker tag yourusername/env-app:1.0.0 yourusername/env-app:staging
docker tag yourusername/env-app:1.0.0 yourusername/env-app:prod

# Push all tags
docker push yourusername/env-app:dev
docker push yourusername/env-app:staging
docker push yourusername/env-app:prod
```

### Tagging Strategy Best Practices

1. **Use semantic versioning** (MAJOR.MINOR.PATCH)
2. **Always tag with specific versions**, not just `latest`
3. **Update `latest` tag** when you push the newest stable version
4. **Use descriptive tags** for special purposes (alpine, slim, etc.)
5. **Consider environment tags** (dev, staging, prod) for deployment pipelines
6. **Document your tagging strategy** in the repository README

## Task 5: Working with Docker Hub Webhooks

### Creating a Webhook Receiver

The webhook receiver from the examples directory is a simple Flask application:

```python
from flask import Flask, request, jsonify
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Log the webhook data
    logging.info(f"Received webhook: {json.dumps(data, indent=2)}")
    
    # Save webhook data to a file for inspection
    with open('last_webhook.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Here you could add automation logic
    # For example, trigger a deployment, send a notification, etc.
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

To run the webhook receiver:

```bash
# Install dependencies
pip install flask

# Run the server
python webhook_receiver.py
```

### Configuring a Webhook in Docker Hub

1. Log in to Docker Hub
2. Navigate to your repository
3. Click on "Webhooks" in the left menu
4. Click "Create Webhook"
5. Enter a name (e.g., "Deployment Trigger")
6. Enter the webhook URL (e.g., `https://your-server.com/webhook`)
7. Click "Create"

For testing locally, you can use tools like `ngrok` to expose your local server:

```bash
# Install ngrok
# Run ngrok to create a tunnel to your local webhook server
ngrok http 5000
```

Use the generated URL (e.g., `https://abc123.ngrok.io/webhook`) in Docker Hub.

### Webhook Payload Example

```json
{
  "callback_url": "https://registry.hub.docker.com/u/username/repository/webhook/webhook_id/results/abc123/",
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

### Use Cases for Webhooks

1. **CI/CD Integration**: Trigger deployments when new images are pushed
2. **Notifications**: Send alerts to Slack, email, etc.
3. **Infrastructure Updates**: Update running containers with new images
4. **Documentation**: Update documentation when new versions are released
5. **Testing**: Trigger tests against new image versions

## Task 6: Automated Builds

### Connecting Docker Hub to GitHub/GitLab

1. Log in to Docker Hub
2. Go to Account Settings > Linked Accounts
3. Click on GitHub (or GitLab)
4. Authorize Docker Hub to access your GitHub account
5. Select the repositories you want to give access to

### Setting Up Automated Builds

1. Go to your Docker Hub repository
2. Click on "Builds" in the left menu
3. Click "Link to GitHub" (or GitLab)
4. Select your GitHub repository
5. Configure build settings:
   - Select the branch to build from (e.g., main)
   - Specify the Dockerfile location
   - Configure the image tag format

### Configuring Build Rules

```
# Example build rules:
# Branch: main, Tag: latest, Dockerfile location: Dockerfile
# Branch: develop, Tag: dev, Dockerfile location: Dockerfile
# Tag: v{sourceref}, Tag: {sourceref}, Dockerfile location: Dockerfile
```

### Testing Automated Builds

1. Make changes to your code in GitHub
2. Commit and push to the configured branch
3. Monitor the build in Docker Hub
4. Verify the new image is created with the correct tag

### Automated Build Benefits

1. **Source-to-image traceability**: Know exactly what code is in each image
2. **Automated workflow**: No manual build and push steps
3. **Consistency**: Every build follows the same process
4. **Versioning**: Automatic tagging based on Git branches/tags
5. **Documentation**: README automatically synced from GitHub

## Task 7: Image Security and Scanning

### Enabling Vulnerability Scanning

1. Log in to Docker Hub
2. Navigate to your repository
3. Click on "Settings" in the left menu
4. Enable "Image Scanning"

Note: Docker Hub's free tier may have limitations on scanning features. Check the current offering.

### Analyzing and Fixing Vulnerabilities

Common vulnerabilities found in Docker images:

1. **Outdated base images**: Update to newer versions
   ```dockerfile
   # Instead of
   FROM ubuntu:18.04
   # Use
   FROM ubuntu:22.04
   ```

2. **Outdated packages**: Update packages during build
   ```dockerfile
   RUN apt-get update && \
       apt-get upgrade -y && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*
   ```

3. **Unnecessary packages**: Remove unneeded packages
   ```dockerfile
   RUN apt-get update && \
       apt-get install --no-install-recommends -y package1 package2 && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*
   ```

4. **Vulnerable dependencies**: Update to patched versions
   ```
   # In requirements.txt
   # Instead of
   flask==1.0.0
   # Use
   flask==2.0.1
   ```

### Docker Hub Security Best Practices

1. **Use specific image tags** instead of `latest`
2. **Enable vulnerability scanning** for all repositories
3. **Regularly update base images** and dependencies
4. **Implement least privilege principle** (non-root users)
5. **Limit access to private repositories** with teams and permissions
6. **Use secrets management** for sensitive data
7. **Implement content trust** for image signing

## Task 8: Working with Docker Hub API

### Generating a Docker Hub Access Token

1. Log in to Docker Hub
2. Go to Account Settings > Security
3. Click "New Access Token"
4. Enter a description (e.g., "API Access")
5. Select appropriate permissions
6. Copy and save the token (it won't be shown again)

### Docker Hub API Python Script

```python
import requests
import os
import json

# Configuration
DOCKER_HUB_USERNAME = "your-username"  # Replace with your username
DOCKER_HUB_TOKEN = "your-token"  # Replace with your token, or use environment variable
# DOCKER_HUB_TOKEN = os.environ.get('DOCKER_HUB_TOKEN')

# Base API URL
API_URL = "https://hub.docker.com/v2"

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DOCKER_HUB_TOKEN}"
}

def list_repositories():
    """List all repositories for the user"""
    url = f"{API_URL}/repositories/{DOCKER_HUB_USERNAME}/"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repositories = response.json()
        print(f"Repositories for {DOCKER_HUB_USERNAME}:")
        for repo in repositories['results']:
            print(f"- {repo['name']}: {repo['description']}")
        return repositories['results']
    else:
        print(f"Error listing repositories: {response.status_code}")
        print(response.text)
        return None

def get_repository_details(repository_name):
    """Get details for a specific repository"""
    url = f"{API_URL}/repositories/{DOCKER_HUB_USERNAME}/{repository_name}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repo = response.json()
        print(f"Details for {DOCKER_HUB_USERNAME}/{repository_name}:")
        print(f"Description: {repo['description']}")
        print(f"Stars: {repo['star_count']}")
        print(f"Pull Count: {repo['pull_count']}")
        print(f"Last Updated: {repo['last_updated']}")
        return repo
    else:
        print(f"Error getting repository details: {response.status_code}")
        print(response.text)
        return None

def list_tags(repository_name):
    """List all tags for a repository"""
    url = f"{API_URL}/repositories/{DOCKER_HUB_USERNAME}/{repository_name}/tags"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        tags = response.json()
        print(f"Tags for {DOCKER_HUB_USERNAME}/{repository_name}:")
        for tag in tags['results']:
            print(f"- {tag['name']}: Last updated {tag['last_updated']}")
        return tags['results']
    else:
        print(f"Error listing tags: {response.status_code}")
        print(response.text)
        return None

def create_repository(repository_name, is_private=False):
    """Create a new repository"""
    url = f"{API_URL}/repositories/"
    data = {
        "namespace": DOCKER_HUB_USERNAME,
        "name": repository_name,
        "is_private": is_private,
        "description": f"Repository created via API for {repository_name}"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print(f"Repository {DOCKER_HUB_USERNAME}/{repository_name} created successfully!")
        return True
    else:
        print(f"Error creating repository: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    # Example usage
    print("Listing all repositories:")
    repos = list_repositories()
    
    if repos and len(repos) > 0:
        # Get details for the first repository
        first_repo = repos[0]['name']
        print(f"\nGetting details for {first_repo}:")
        repo_details = get_repository_details(first_repo)
        
        print(f"\nListing tags for {first_repo}:")
        tags = list_tags(first_repo)
    
    # Uncomment to create a new repository
    # create_repository("test-api-repo", is_private=True)
```

### Using the Docker Hub API

To run the script:
```bash
# Set token as environment variable (recommended for security)
export DOCKER_HUB_TOKEN="your-token"

# Run the script
python dockerhub_api.py
```

### Additional API Operations

The Docker Hub API allows for:
- Creating/deleting repositories
- Managing tags and images
- Setting up webhooks
- Managing organizations and teams
- Configuring automated builds

## Task 9: Docker Hub Organizations and Teams

### Docker Hub Organizations

Organizations in Docker Hub allow teams to collaborate on Docker images with:
- Centralized access control
- Shared billing
- Team-based permissions
- Audit logs

### Creating an Organization

1. Log in to Docker Hub
2. Click on "Organizations" in the top menu
3. Click "Create Organization"
4. Enter organization name and email
5. Select a plan
6. Click "Create"

### Managing Teams

1. Navigate to your organization
2. Click on "Teams" in the left menu
3. Click "Create Team"
4. Enter a team name (e.g., "developers", "operations")
5. Add members by username or email
6. Set permissions (read, write, admin)

### Organization Permission Structure

- **Owners**: Full access to all repositories and settings
- **Team Admin**: Can manage team membership
- **Team Member**: Access based on team permissions

For each repository:
- **Read**: Pull images
- **Write**: Push and pull images
- **Admin**: Push, pull, and change repository settings

### Setting Up Organization Structure

```
Organization: Example Corp
├── Teams:
│   ├── Developers
│   │   ├── Permission: Read/Write to dev repositories
│   │   └── Members: developer1, developer2
│   ├── Operations
│   │   ├── Permission: Read to all, Write to prod repositories
│   │   └── Members: ops1, ops2
│   └── Admins
│       ├── Permission: Admin to all repositories
│       └── Members: admin1, admin2
└── Repositories:
    ├── app-dev
    │   └── Teams: Developers (Write), Operations (Read)
    ├── app-prod
    │   └── Teams: Operations (Write), Developers (Read)
    └── base-images
        └── Teams: Admins (Admin), Developers (Read), Operations (Read)
```

## Task 10: Real-world Docker Hub Integration

### CI/CD Pipeline with Docker Hub

Example GitHub Actions workflow:

```yaml
name: Build and Push to Docker Hub

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to DockerHub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: yourusername/app-name
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=ref,event=branch
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v3
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=yourusername/app-name:buildcache
          cache-to: type=registry,ref=yourusername/app-name:buildcache,mode=max
```

### Image Lifecycle Management

Best practices:
1. **Retention policy**: Automatically delete unused or old image versions
2. **Vulnerability monitoring**: Regularly scan images and fix issues
3. **Promotion workflow**: Promote images through environments (dev -> test -> prod)
4. **Version control**: Use semantic versioning and clear tagging
5. **Documentation**: Keep README and description up to date

### Deployment Workflow Example

```bash
#!/bin/bash
# Script to deploy the latest Docker image from Docker Hub

# Configuration
REPO_NAME="yourusername/app-name"
CONTAINER_NAME="app-container"
DOCKER_NETWORK="app-network"
TAG="latest"  # or specific version

# Pull the latest image
echo "Pulling $REPO_NAME:$TAG from Docker Hub..."
docker pull $REPO_NAME:$TAG

# Stop and remove existing container
echo "Stopping existing container if running..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Create network if it doesn't exist
docker network inspect $DOCKER_NETWORK >/dev/null 2>&1 || \
    docker network create $DOCKER_NETWORK

# Run the new container
echo "Starting new container..."
docker run -d \
    --name $CONTAINER_NAME \
    --network $DOCKER_NETWORK \
    -p 8080:8080 \
    -e "ENV=production" \
    $REPO_NAME:$TAG

echo "Deployment completed successfully!"
```

### Real-world Integration Best Practices

1. **Automation**: Automate all image building, pushing, and deployment
2. **Security**: Implement scanning, signing, and least privilege
3. **Documentation**: Keep README, tags, and descriptions up to date
4. **Monitoring**: Monitor image usage, pulls, and deployments
5. **Testing**: Test images before promoting to production repositories
6. **Version control**: Use clear tagging strategies tied to source code
7. **Access control**: Implement proper permissions and team structure 