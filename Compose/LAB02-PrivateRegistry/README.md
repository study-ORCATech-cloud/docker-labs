# LAB02: Private Registry with Nexus

This lab guides you through setting up a private Docker registry using Sonatype Nexus, building a simple Flask application, and pushing/pulling Docker images from your private registry.

## Lab Overview

In this lab, you will:
- Set up a Nexus repository manager using Docker Compose
- Configure it as a private Docker registry
- Build and push a custom Flask application image
- Pull and run the image from your private registry
- Learn about registry security and configuration

## Learning Objectives

- Understand the purpose and benefits of private Docker registries
- Set up and configure Nexus as a Docker registry
- Build, tag, and push images to a private registry
- Pull and deploy images from a private registry
- Configure Docker to work with insecure registries
- Implement basic security for private registries

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic knowledge of Docker commands
- Completion of LAB01-ServiceCommunication (recommended)

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Local Docker   │     │  Nexus Docker   │     │   Container     │
│     Client      │────▶│    Registry     │────▶│  from Registry  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
    Push/Pull             Port 8082              Flask App on
    Images                                        Port 5000
```

## Project Files

- `docker-compose.yaml` - Configuration for the Nexus container
- `docker-compose-service1.yaml` - Configuration to run the service from the registry
- `Dockerfile` - Instructions to build the Flask application image
- `src/main.py` - Simple Flask application with health checks
- `requirements.txt` - Python dependencies for the Flask application

---

## Lab Steps

### 1. Start Nexus Repository Manager

With your `docker-compose.yaml` in place, start Nexus by running:

```bash
docker-compose up -d
```

This command:
1. Starts the Nexus container in detached mode
2. Exposes the Nexus UI on port `8081` and the Docker repository on port `8082`
3. Sets up a persistent volume for Nexus data

You can check if the container is running with:

```bash
docker ps
```

> **Note:** Nexus may take a minute or two to fully start up. Be patient if you can't access the UI immediately.

---

## **2. Access Nexus UI**

Once Nexus is running, access the web interface at:

- **Nexus UI:** [http://localhost:8081](http://localhost:8081)
  - **Username:** `admin`
  - **Password:** `admin123` (as set in docker-compose.yaml with `NEXUS_SECURITY_RANDOMPASSWORD=false`)

> **Tip:** If you're using Nexus in a production environment, make sure to change the default password for security reasons.

### First-time Login

If this is your first time logging in:
1. You may be prompted to complete initial setup
2. You might need to change the default password
3. You might need to accept the license agreement
4. When prompted to select whether to allow anonymous pulling or not, you can choose either

---

## **3. Create the Docker Repository**

Now we need to set up a Docker repository in Nexus:

1. After logging in, click on the gear icon (⚙️) in the top menu to access **"Administration"**
2. In the left sidebar, navigate to **"Repositories"**
3. Click the **"Create repository"** button
4. Select **"Docker (hosted)"** from the list of repository recipes
5. Fill in the following details:
   - **Name:** `docker-hosted` (or any name you prefer)
   - **HTTP:** Check this box and enter port `8082`
   - **Allow anonymous docker pull:** You can enable this for testing, but disable in production
   - **Storage:** Leave default settings
6. Click **"Create repository"** to save your configuration

> **Note:** The HTTP port (8082) must match the port exposed in your docker-compose.yaml file.

---

## **4. Enable Docker Private Registry in Docker Engine**

Since our docker registry runs on HTTP (not HTTPS), we need to configure Docker to allow this insecure connection:

### For Docker Desktop (Windows/Mac):

1. Open Docker Desktop
2. Click on "Settings" (gear icon)
3. Select "Docker Engine" from the sidebar
4. In the JSON configuration, add `"localhost:8082"` to the `"insecure-registries"` array:
   ```json
   {
     "insecure-registries": ["localhost:8082"],
     // other settings...
   }
   ```
5. Click "Apply & restart"

### For Linux:

1. Edit the Docker daemon configuration:
   ```bash
   sudo nano /etc/docker/daemon.json
   ```
2. Add or modify the "insecure-registries" section:
   ```json
   {
     "insecure-registries": ["localhost:8082"]
   }
   ```
3. Save the file and restart Docker:
   ```bash
   sudo systemctl restart docker
   ```

---

## **5. Build and Push Your Service to Nexus**

Our project contains a simple Flask application with health checks and a welcome endpoint.

### 5.1 Examine the Application

The Flask application (`src/main.py`) provides:
- A `/welcome` endpoint that returns a greeting message
- Health check endpoints (`/liveness` and `/readiness`)
- A `/welcomeFail` endpoint for testing error responses

### 5.2 Build the Service Image

First, build the Docker image for our Flask application:

```bash
# From the root directory of this project
docker build -t service1:1.0 .
```

This builds the image using the Dockerfile, which:
- Uses Python 3.12-slim as the base image
- Sets up a non-root user for security
- Installs the Flask dependencies
- Configures the application to run on startup

### 5.2 Tag the Image for Nexus

Tag your Docker image to match the Nexus repository URL:

```bash
docker tag service1:1.0 localhost:8082/service1:1.0
```

### 5.3 Log in to Nexus Docker Repository

Log in to the Nexus repository using Docker CLI:

```bash
docker login localhost:8082
```

Enter your Nexus credentials:
- **Username:** `admin`
- **Password:** `admin123`

You should see "Login Succeeded" if everything worked correctly.

### 5.4 Push the Image to Nexus

Push your Docker image to the Nexus repository:

```bash
docker push localhost:8082/service1:1.0
```

You should see the progress as Docker uploads the image layers to Nexus.

After pushing, you can verify the image is in Nexus by browsing to:
- **Nexus UI** → **Browse** → **docker-hosted** repository

---

## **6. Remove Local Image**

To simulate pulling from the private registry in a real-world scenario, remove both the local images:

```bash
docker rmi localhost:8082/service1:1.0 service1:1.0
```

Verify the images are gone:

```bash
docker images | grep service1
```

---

## **7. Run Service from Private Registry**

Now let's run our service by pulling it from our private Nexus registry:

```bash
docker-compose -f docker-compose-service1.yaml -p service1 up
```

This command:
1. Uses our service-specific compose file
2. Creates a project named "service1"
3. Automatically pulls the image from localhost:8082
4. Runs the container with the specified environment variables
5. Maps port 5000 to access our Flask application

### 7.1 Testing the Service

Once the service is running, test it with:

```bash
# Test the welcome endpoint
curl http://localhost:5000/welcome

# Test the health checks
curl http://localhost:5000/liveness
curl http://localhost:5000/readiness
```

You should receive JSON responses from each endpoint.

---

## Real-World Applications

Private Docker registries like Nexus provide many benefits in production environments:

- **Security**: Control access to your private images
- **Network Efficiency**: Reduce bandwidth by keeping images on your local network
- **Availability**: Ensure images are available even if external registries are down
- **Versioning**: Maintain control over image versions and tags
- **Compliance**: Meet regulatory requirements for controlling software distribution

## Troubleshooting

### Cannot access Nexus UI
- Ensure the Nexus container is running: `docker ps`
- Check Nexus logs: `docker logs nexus`
- Verify your firewall isn't blocking port 8081

### Cannot push to registry
- Verify you've configured Docker for insecure registries correctly
- Ensure you've logged in with the correct credentials
- Check if the repository was created properly in Nexus
- Try restarting Docker service

### Service doesn't start correctly
- Check that the image was pulled successfully
- Verify the port mappings in docker-compose-service1.yaml
- Check service logs with `docker-compose -f docker-compose-service1.yaml logs`

---

## **Cleaning Up**

When you're done with the lab, you can clean up with:

```bash
# Stop the service
docker-compose -f docker-compose-service1.yaml -p service1 down

# Stop Nexus
docker-compose down

# To also remove the Nexus data volume (caution: this deletes all data!)
docker-compose down -v
```
