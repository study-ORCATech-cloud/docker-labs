# AutoBuild Demo Application

A sample Python Flask application demonstrating Docker Hub automated builds from GitHub/GitLab.

## Features

- Simple web API with health check and info endpoints
- Docker Hub automated builds integration
- Build-time arguments for versioning and traceability
- Docker best practices implementation

## Docker Image

This image is automatically built from the GitHub repository whenever changes are pushed. The Docker Hub repository is configured with build rules:

- `latest`: Built from the `main` branch
- Version tags (e.g., `1.0.0`): Built from git tags matching the pattern `v*`
- `dev`: Built from the `develop` branch

## Usage

### Pull the Image

```bash
docker pull yourusername/autobuild-demo:latest
```

### Run the Container

```bash
docker run -p 8080:8080 yourusername/autobuild-demo:latest
```

### Environment Variables

The following environment variables can be set:

- `APP_VERSION`: Application version (default: 1.0.0)
- `ENVIRONMENT`: Deployment environment (default: production)
- `PORT`: Port to listen on (default: 8080)

Example:
```bash
docker run -p 8080:8080 \
  -e APP_VERSION=1.1.0 \
  -e ENVIRONMENT=staging \
  -e PORT=8080 \
  yourusername/autobuild-demo:latest
```

## API Endpoints

- `GET /`: Main application information
- `GET /health`: Health check endpoint
- `GET /info`: Detailed application information

## Local Development

### Build the Image Locally

```bash
docker build -t autobuild-demo:local .
```

### Using Docker Compose

```bash
docker-compose up
```

## Build Arguments

This image uses the following build arguments:

- `GIT_COMMIT`: Git commit hash (set automatically in Docker Hub builds)
- `BUILD_DATE`: Build timestamp (set automatically in Docker Hub builds)
- `APP_VERSION`: Application version

## License

MIT

## About

This is a sample application for the Docker Hub Automated Builds lab exercise. 