# LAB05: Scaling Services with Docker Compose

This lab demonstrates how to scale services using Docker Compose for handling increased load and providing high availability.

## Learning Objectives

- Configure services for horizontal scaling
- Use Docker Compose to scale services
- Implement load balancing with a reverse proxy
- Monitor scaled services
- Understand container replica management

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker containers
- Familiarity with YAML syntax

## Lab Environment

In this lab, we'll create a simple Python web application that can be scaled, a Redis database for storing visit counts, and a Nginx load balancer to distribute traffic across the web application instances.

## Lab Steps

### Step 1: Setup Project Structure

Create the following directory structure:

```
LAB05-ScalingServices/
├── docker-compose.yml
├── web/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── nginx/
    └── nginx.conf
```

### Step 2: Create the Python Web Application

1. Create `web/app.py`:

```python
from flask import Flask
import redis
import socket
import os

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    hostname = socket.gethostname()
    return f'Hello World! I have been seen {count} times.<br>Container ID: {hostname}'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

2. Create `web/requirements.txt`:

```
flask==2.0.1
redis==3.5.3
```

3. Create `web/Dockerfile`:

```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### Step 3: Configure Nginx as Load Balancer

Create `nginx/nginx.conf`:

```
events {
    worker_connections 1024;
}

http {
    upstream web-app {
        server web:5000;
    }
    
    server {
        listen 80;
        
        location / {
            proxy_pass http://web-app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### Step 4: Create Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: ./web
    ports:
      - "5000"
    depends_on:
      - redis
    environment:
      - FLASK_ENV=development
    deploy:
      replicas: 1
    networks:
      - webnet

  redis:
    image: redis:6.2-alpine
    networks:
      - webnet
    volumes:
      - redis-data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - webnet

networks:
  webnet:

volumes:
  redis-data:
```

### Step 5: Start the Application

```bash
docker-compose up -d
```

This will start one instance of the web service, Redis, and Nginx.

### Step 6: Scale the Web Service

Now let's scale the web service to 5 instances:

```bash
docker-compose up -d --scale web=5
```

Docker Compose will start 4 additional containers for the web service.

### Step 7: Test the Load Balancing

Open a web browser and navigate to http://localhost/ multiple times. You should see the container ID change as requests are distributed across different web service instances.

You can also use a command line tool to test:

```bash
for i in {1..10}; do curl http://localhost/; echo; done
```

### Step 8: Monitoring Containers

View running containers and their resource usage:

```bash
docker-compose ps
docker stats
```

### Step 9: Dynamically Adjust Scale

You can adjust the number of containers at any time:

```bash
# Scale up to 10 instances
docker-compose up -d --scale web=10

# Scale down to 3 instances
docker-compose up -d --scale web=3
```

## Advanced Scaling Techniques

### Auto-Scaling with Watchtower (Optional)

For production environments, you might want to implement auto-scaling based on metrics. While Docker Compose itself doesn't support auto-scaling, you can use additional tools.

Here's a basic implementation of auto-scaling using a Python script:

Create a file called `autoscale.py` in the root of your project:

```python
import time
import subprocess
import docker

client = docker.from_env()

def get_cpu_usage(container):
    stats = container.stats(stream=False)
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    if system_delta > 0:
        return (cpu_delta / system_delta) * 100
    return 0

def get_average_cpu(service_name):
    containers = client.containers.list(filters={"label": f"com.docker.compose.service={service_name}"})
    if not containers:
        return 0
    total_cpu = sum(get_cpu_usage(container) for container in containers)
    return total_cpu / len(containers)

def scale_service(service_name, replicas):
    subprocess.run(["docker", "compose", "up", "-d", "--scale", f"{service_name}={replicas}"])
    print(f"Scaled {service_name} to {replicas} replicas")

def autoscale():
    min_replicas = 2
    max_replicas = 10
    scale_up_threshold = 70  # CPU percentage
    scale_down_threshold = 30  # CPU percentage
    service_name = "web"
    
    while True:
        try:
            avg_cpu = get_average_cpu(service_name)
            current_replicas = len(client.containers.list(filters={"label": f"com.docker.compose.service={service_name}"}))
            
            print(f"Service: {service_name}, Replicas: {current_replicas}, Avg CPU: {avg_cpu:.2f}%")
            
            if avg_cpu > scale_up_threshold and current_replicas < max_replicas:
                scale_service(service_name, current_replicas + 1)
            elif avg_cpu < scale_down_threshold and current_replicas > min_replicas:
                scale_service(service_name, current_replicas - 1)
                
            time.sleep(30)  # Check every 30 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait longer if there's an error

if __name__ == "__main__":
    autoscale()
```

To use this script, you'd need to install the Docker Python SDK:

```bash
pip install docker
```

Then run the autoscaling script:

```bash
python autoscale.py
```

## Cleanup

To stop and remove all containers, networks, and volumes created by Docker Compose:

```bash
docker-compose down -v
```

This will stop all services and remove the containers, networks, and volumes defined in the Docker Compose file.

To remove only the containers while keeping the volumes:

```bash
docker-compose down
```

## Conclusion

In this lab, you learned how to:
- Configure a scalable application with Docker Compose
- Use the `--scale` option to adjust service replicas
- Set up a load balancer to distribute traffic
- Monitor container performance
- Implement a basic auto-scaling mechanism

Scaling with Docker Compose provides a simple way to handle increased load for applications in development or small production environments. For more robust scaling in production, consider using container orchestration platforms like Kubernetes. 