# LAB01: Service Communication with Docker Compose - Solutions

This document provides reference solutions to the Docker Compose exercises in LAB01-ServiceCommunication. These solutions are meant to be reviewed **after** you have attempted to solve the exercises yourself.

Compare your implementations with these solutions to understand different approaches and best practices for Docker Compose service communication.

## docker-compose.yaml Solution

```yaml
version: "3.8"

services:
  service1:
    build:
      context: ./service1
      dockerfile: Dockerfile  # Default name, but explicitly stated
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - SERVICE2_NAME=hibye
    depends_on:
      - hibye

  hibye:
    build:
      context: ./service2
      dockerfile: chokomoko  # Custom Dockerfile name
    ports:
      - "5001:5001"
    environment:
      - PORT=5001
```

## docker-compose-isolated.yaml Solution

```yaml
version: "3.8"

services:
  service1:
    build:
      context: ./service1
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - SERVICE2_NAME=hibye
    networks:
      - network1

  hibye:
    build:
      context: ./service2
      dockerfile: chokomoko
    ports:
      - "5001:5001"
    environment:
      - PORT=5001
    networks:
      - network2

networks:
  network1:
    driver: bridge
  network2:
    driver: bridge
```

## Exercise 3: Solution for Connecting Isolated Services

### Option 1: Connect a Service to Multiple Networks

Modify docker-compose-isolated.yaml:

```yaml
version: "3.8"

services:
  service1:
    build:
      context: ./service1
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - SERVICE2_NAME=hibye
    networks:
      - network1
      - network2  # Added network2 to enable communication

  hibye:
    build:
      context: ./service2
      dockerfile: chokomoko
    ports:
      - "5001:5001"
    environment:
      - PORT=5001
    networks:
      - network2

networks:
  network1:
    driver: bridge
  network2:
    driver: bridge
```

### Option 2: Using Docker Network Connect

Command to connect an existing container to network2:

```sh
docker network connect network2 lab01servicecommunication-service1-1
```

## Part 5: Additional Challenges - Solutions

### 1. Implementing Service Discovery

```yaml
version: "3.8"

services:
  service1:
    build:
      context: ./service1
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - SERVICE2_NAME=hibye
    depends_on:
      - hibye
    # DNS-based service discovery happens automatically with Docker Compose
    # No additional configuration needed

  hibye:
    build:
      context: ./service2
      dockerfile: chokomoko
    ports:
      - "5001:5001"
    environment:
      - PORT=5001
```

### 2. Adding a Third Service

```yaml
version: "3.8"

services:
  service1:
    build:
      context: ./service1
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - SERVICE2_NAME=hibye
    depends_on:
      - hibye

  hibye:
    build:
      context: ./service2
      dockerfile: chokomoko
    ports:
      - "5001:5001"
    environment:
      - PORT=5001

  aggregator:
    build:
      context: ./aggregator  # New directory would need to be created
      dockerfile: Dockerfile
    ports:
      - "5002:5002"
    environment:
      - PORT=5002
      - SERVICE1_URL=http://service1:5000
      - SERVICE2_URL=http://hibye:5001
    depends_on:
      - service1
      - hibye
```

### 3. Implementing a Bridge Service

```yaml
version: "3.8"

services:
  service1:
    build:
      context: ./service1
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - BRIDGE_SERVICE_URL=http://bridge:5050
    networks:
      - network1
    depends_on:
      - bridge

  hibye:
    build:
      context: ./service2
      dockerfile: chokomoko
    ports:
      - "5001:5001"
    environment:
      - PORT=5001
    networks:
      - network2
    depends_on:
      - bridge

  bridge:
    build:
      context: ./bridge  # New directory would need to be created
      dockerfile: Dockerfile
    ports:
      - "5050:5050"
    environment:
      - PORT=5050
      - SERVICE2_URL=http://hibye:5001
    networks:
      - network1
      - network2

networks:
  network1:
    driver: bridge
  network2:
    driver: bridge
```

## Key Learning Points

### Service Names as Hostnames
Docker Compose automatically sets up DNS resolution so that service names can be used as hostnames within the Docker Compose network.

### Default Network
By default, Docker Compose creates a single network for all services, which allows them to communicate freely with each other.

### Custom Networks
Custom networks allow for isolation and segmentation of services. This is crucial for security in production environments.

### Service Dependencies
The `depends_on` parameter ensures services start in the correct order but doesn't guarantee application readiness. For proper application-level readiness, you would need health checks.

### Network Bridging Techniques
Multiple approaches exist to connect isolated services:
- Multi-network service connections
- Runtime network connects with `docker network connect`
- Bridge services acting as proxies

## Common Questions and Answers

**Q**: Why use custom service names like "hibye" instead of just "service2"?  
**A**: Custom names allow for more descriptive service identification and are often used in real-world scenarios to give names that reflect the service's purpose.

**Q**: How does service discovery work in Docker Compose?  
**A**: Docker Compose sets up internal DNS resolution so services can find each other by service name. This happens automatically within the default network.

**Q**: Can I have more than two networks?  
**A**: Yes, you can create as many networks as needed for complex segmentation scenarios.

**Q**: What happens if I try to connect to a service in an isolated network?  
**A**: You'll get connection refused or timeout errors because there's no network path between the containers.

## Advanced Techniques to Explore

1. **Scaling Services**: Try using `docker-compose up --scale hibye=3` to create multiple instances of a service and observe the load balancing behavior.

2. **Network Policies**: Experiment with more complex network topologies with multiple isolated service groups.

3. **Service Meshes**: Explore how basic service mesh concepts can be implemented using proxy services. 