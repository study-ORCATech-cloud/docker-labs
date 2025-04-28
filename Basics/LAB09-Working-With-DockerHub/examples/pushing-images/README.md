# Building and Pushing Images to Docker Hub

This directory contains examples and instructions for building, tagging, and pushing Docker images to Docker Hub.

## Prerequisites

Before you can push images to Docker Hub, you need:
1. A Docker Hub account
2. Docker CLI installed and logged in to your Docker Hub account
3. A repository created on Docker Hub

## Understanding Docker Image Names and Tags

Docker images are referenced using the format:
```
[registry/]username/repository:tag
```

- **registry**: Specifies a registry other than Docker Hub (optional, defaults to Docker Hub)
- **username**: Your Docker Hub username
- **repository**: The repository name
- **tag**: A specific version or variant of the image (optional, defaults to "latest")

Examples:
- `username/myapp:1.0`
- `username/myapp:latest`
- `registry.example.com/username/myapp:1.0`

## Building a Docker Image

Navigate to the directory containing your Dockerfile:

```bash
# Build the image with a tag
docker build -t yourusername/repository-name:tag .
```

For example:
```bash
docker build -t yourusername/python-web-app:v1.0 .
```

## Tagging an Existing Image

If you've already built an image, you can tag it:

```bash
# Tag an existing image
docker tag source-image:tag yourusername/repository-name:tag
```

For example:
```bash
docker tag myapp:1.0 yourusername/python-web-app:v1.0
```

You can add multiple tags to the same image:
```bash
docker tag yourusername/python-web-app:v1.0 yourusername/python-web-app:latest
```

## Pushing Images to Docker Hub

Once you've built and tagged your image, push it to Docker Hub:

```bash
# Push the image to Docker Hub
docker push yourusername/repository-name:tag
```

For example:
```bash
docker push yourusername/python-web-app:v1.0
```

If you have multiple tags, push each one:
```bash
docker push yourusername/python-web-app:latest
```

## Verifying Your Push

After pushing, verify that your image appears on Docker Hub:
1. Log in to Docker Hub
2. Navigate to your repository
3. Click on the "Tags" tab
4. You should see your newly pushed image

## Updating and Pushing a New Version

When you make changes to your application:
1. Update your code
2. Build a new image with a new tag
3. Push the new image to Docker Hub

```bash
# Build with new version tag
docker build -t yourusername/python-web-app:v1.1 .

# Push the new version
docker push yourusername/python-web-app:v1.1

# Update and push the latest tag
docker tag yourusername/python-web-app:v1.1 yourusername/python-web-app:latest
docker push yourusername/python-web-app:latest
```

## Sample Python Application

This directory includes a simple Python Flask application:

- `app.py`: A simple web server
- `requirements.txt`: Python dependencies
- `Dockerfile`: Instructions to build the image

## Working with the Sample Application

```bash
# Build the image
docker build -t yourusername/python-demo:v1.0 .

# Test the image locally
docker run -p 8080:8080 yourusername/python-demo:v1.0

# Push to Docker Hub
docker push yourusername/python-demo:v1.0
```

## Common Issues

- **Authentication failure**: Ensure you're logged in with `docker login`
- **Permission denied**: Verify you have write access to the repository
- **Name unknown**: Check for typos in the repository name
- **Tag already exists**: You can overwrite an existing tag, or use a new tag
- **Rate limiting**: Docker Hub enforces pull rate limits for free accounts

## TODO

Complete the following tasks:
1. Build the provided Dockerfile to create a simple image
2. Tag the image according to Docker Hub conventions
3. Push the image to your Docker Hub repository
4. Verify the image appears in your Docker Hub repository
5. Make a small change to the application code and push a new version
6. Document your experience and any issues you encountered in `push_notes.md` 