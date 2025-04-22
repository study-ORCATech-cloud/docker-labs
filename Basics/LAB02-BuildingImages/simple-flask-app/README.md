# Simple Flask Application

This is a basic Flask web application designed to demonstrate simple Docker containerization concepts.

## Features

- Basic web interface that confirms the app is running
- Health check endpoint
- Containerized using Docker

## Docker Commands

Build the image:
```bash
docker build -t simple-flask-app:1.0 .
```

Run the container:
```bash
docker run -d -p 5000:5000 --name flask-demo simple-flask-app:1.0
```

Test the application:
```bash
curl http://localhost:5000
curl http://localhost:5000/health
```

## Dockerfile Explanation

The `Dockerfile` in this example demonstrates:
- Using a specific base image (`python:3.9-slim`)
- Setting up a working directory (`WORKDIR /app`)
- Copying and installing dependencies before copying the application code (for better layer caching)
- Exposing the application port (`EXPOSE 5000`)
- Setting the default command (`CMD ["python", "app.py"]`) 