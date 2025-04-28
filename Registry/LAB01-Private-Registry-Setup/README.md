# LAB01: Setting Up a Local Docker Registry

This lab will guide you through setting up and using a local Docker registry to store and distribute your Docker images.

## Lab Overview

In this lab, you will:
- Set up a private Docker registry container
- Configure registry persistence and security
- Push and pull images to/from your private registry
- Explore registry API endpoints
- Implement basic authentication
- Understand registry storage options

## Learning Objectives

- Understand Docker Registry concepts
- Set up a local Docker registry container
- Push and pull images from your private registry
- Configure basic authentication
- Understand registry storage options
- Use Docker Compose to manage the registry

## Prerequisites

- Docker Engine installed
- Docker Compose installed
- Completion of Docker Basics labs
- Basic familiarity with Docker images and containers

## Lab Tasks

### Task 1: Run a Simple Registry Container

Start a simple registry container:

```bash
docker run -d -p 5000:5000 --name registry registry:2
```

Verify it's running:

```bash
docker ps
```

### Task 2: Push an Image to Your Local Registry

First, pull an image to use:

```bash
docker pull nginx
```

Tag the image for your local registry:

```bash
docker tag nginx localhost:5000/my-nginx
```

Push the image to your local registry:

```bash
docker push localhost:5000/my-nginx
```

### Task 3: Pull an Image from Your Registry

Remove the local image to simulate pulling from the registry:

```bash
docker image remove nginx
docker image remove localhost:5000/my-nginx
```

Pull the image from your local registry:

```bash
docker pull localhost:5000/my-nginx
```

Run a container using the image:

```bash
docker run -d -p 8080:80 localhost:5000/my-nginx
```

### Task 4: Set Up a Registry with Persistence

Stop and remove the basic registry:

```bash
docker stop registry
docker rm registry
```

Create a directory for registry data:

```bash
mkdir -p registry-data
```

Create a `docker-compose.yml` file:

```yaml
version: '3'

services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    volumes:
      - ./registry-data:/var/lib/registry
    restart: always

volumes:
  registry-data:
    driver: local
```

Start the registry using Docker Compose:

```bash
docker compose up -d
```

### Task 5: Add Basic Authentication

Create a password file:

```bash
mkdir auth
docker run --entrypoint htpasswd registry:2 -Bbn username password > auth/htpasswd
```

Update your `docker-compose.yml`:

```yaml
version: '3'

services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: "Registry Realm"
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
    volumes:
      - ./registry-data:/var/lib/registry
      - ./auth:/auth
    restart: always

volumes:
  registry-data:
    driver: local
```

Restart the registry:

```bash
docker compose down
docker compose up -d
```

Login to your registry:

```bash
docker login localhost:5000
```

Enter the username and password you set earlier.

### Task 6: Explore Registry API

Query the registry API:

```bash
curl -X GET http://localhost:5000/v2/_catalog
```

Get the list of tags for an image:

```bash
curl -X GET http://localhost:5000/v2/my-nginx/tags/list
```

### Task 7: Clean Up

Log out from the registry:

```bash
docker logout localhost:5000
```

Stop the registry:

```bash
docker compose down
```

## Real-World Applications

Private Docker registries are essential in enterprise environments for:

- **Control**: Managing proprietary images and applications
- **Security**: Storing images behind the company firewall
- **Compliance**: Meeting regulatory requirements about software distribution
- **Performance**: Faster image deployments within your network
- **CI/CD Integration**: Streamlining development workflows

## Conclusion

In this lab, you've learned:
- How to set up a private Docker registry
- Pushing and pulling images from your registry
- Adding persistence to the registry
- Configuring basic authentication
- Using the registry API

## Next Steps

- Explore registry configuration options
- Set up a secure registry with TLS certificates
- Implement external storage backends (S3, Azure, etc.)
- Integrate with CI/CD pipelines 