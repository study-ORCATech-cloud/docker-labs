# LAB10: Advanced Networking in Docker Compose

This lab explores advanced networking concepts in Docker Compose, demonstrating how to configure and manage complex network topologies for multi-container applications.

## Learning Objectives

- Master Docker Compose network creation and configuration
- Understand network drivers and their use cases
- Implement service discovery and DNS resolution between containers
- Configure network aliases and custom hostnames
- Create isolated network segments for multi-tier applications
- Implement network policies and access control
- Learn network troubleshooting and debugging techniques
- Configure external network integration
- Implement cross-service communication patterns

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of networking concepts
- Familiarity with Docker Compose from previous labs
- Basic Python knowledge (for sample applications)

## Network Concepts in Docker Compose

Docker Compose provides powerful networking capabilities:

1. **Default Networks**: Every Compose application gets a default network
2. **Custom Networks**: Define application-specific network topologies
3. **Network Drivers**: Bridge, overlay, macvlan, host, and none drivers for different use cases
4. **Service Discovery**: Automatic DNS resolution between services
5. **Network Aliases**: Custom DNS names for services
6. **Network Isolation**: Segmentation of multi-tier applications

## Lab Exercises

### Exercise 1: Basic Network Configuration

Learn the fundamentals of Docker Compose networks with a simple web application and database.

1. Create a basic network configuration
2. Understand default network behavior
3. Configure custom networks with the bridge driver
4. Test service discovery between containers

### Exercise 2: Multi-Tier Application Networks

Build a multi-tier application with isolated network segments.

1. Create separate networks for frontend, backend, and database tiers
2. Configure services to connect to multiple networks
3. Implement network isolation policies
4. Test communication between tiers

### Exercise 3: Advanced Service Discovery

Explore advanced service discovery patterns with DNS and network aliases.

1. Configure network aliases for services
2. Implement load balancing with multiple instances
3. Use custom DNS configurations
4. Test failover and service discovery mechanisms

### Exercise 4: Real-World Microservices Networking

Implement a complex microservices application with sophisticated networking.

1. Create a gateway/API pattern with network segmentation
2. Implement service-to-service communication
3. Configure external network access
4. Secure network communication between services

## Network Drivers

This lab will explore various network drivers:

- **bridge**: The default driver for single-host networking
- **overlay**: For multi-host networking (mentioned but not implemented in this lab)
- **host**: For using the host's networking directly
- **none**: For completely isolated containers
- **macvlan**: For assigning MAC addresses to containers (mentioned but not implemented)

## Project Structure

```
LAB10-ComposeNetworking/
├── exercise1/
│   ├── app/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   ├── docker-compose.yml
│   └── README.md
├── exercise2/
│   ├── frontend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   ├── backend/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── docker-compose.yml
│   └── README.md
├── exercise3/
│   ├── api/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── client/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   ├── docker-compose.yml
│   └── README.md
├── exercise4/
│   ├── gateway/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── users-service/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── products-service/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── db-service/
│   │   └── init-scripts/
│   │       └── init.sql
│   ├── docker-compose.yml
│   └── README.md
└── README.md
```

## Detailed Lab Steps

### Exercise 1: Basic Network Configuration

This exercise introduces the basic concepts of networking in Docker Compose using a simple web application and a Redis backend.

#### Step 1: Examine the Docker Compose Configuration

```bash
cd exercise1
cat docker-compose.yml
```

Notice how the `web` and `redis` services are defined with the default network. Also note how the ports are mapped and how the services communicate.

#### Step 2: Start the Services

```bash
docker compose up -d
```

#### Step 3: Test Service Discovery

```bash
docker compose exec web python -c "import socket; print(socket.gethostbyname('redis'))"
```

This command resolves the hostname 'redis' to an IP address, demonstrating Docker's built-in DNS resolution.

#### Step 4: Create a Custom Network

Modify the docker-compose.yml file to define a custom network:

```yaml
networks:
  app-network:
    driver: bridge
```

And update the services to use this network:

```yaml
services:
  web:
    ...
    networks:
      - app-network
  redis:
    ...
    networks:
      - app-network
```

#### Step 5: Access the Application

Access the web application at http://localhost:8000 to see the counter incrementing. The `web` service communicates with `redis` over the network to store the count.

### Exercise 2: Multi-Tier Application Networks

This exercise demonstrates how to create separate networks for different tiers of an application.

#### Step 1: Examine the Network Configuration

```bash
cd ../exercise2
cat docker-compose.yml
```

Notice the three defined networks: `frontend-network`, `backend-network`, and `db-network`. Also note how services are connected to multiple networks as needed.

#### Step 2: Start the Services

```bash
docker compose up -d
```

#### Step 3: Test Network Isolation

```bash
docker compose exec frontend ping backend
docker compose exec frontend ping db
```

You'll see that `frontend` can reach `backend` but not `db`, demonstrating network isolation.

#### Step 4: Test Multi-Network Communication

```bash
docker compose exec backend ping frontend
docker compose exec backend ping db
```

The `backend` service can communicate with both `frontend` and `db` because it's connected to both networks.

#### Step 5: Access the Application

Access the application at http://localhost:8000 to see it working. The frontend communicates with the backend, which in turn communicates with the database.

### Exercise 3: Advanced Service Discovery

This exercise focuses on advanced service discovery mechanisms with DNS and network aliases.

#### Step 1: Examine the Docker Compose Configuration

```bash
cd ../exercise3
cat docker-compose.yml
```

Notice the `api` service has multiple instances and uses network aliases.

#### Step 2: Start the Services

```bash
docker compose up -d
```

#### Step 3: Test Service Discovery with Aliases

```bash
docker compose exec client ping api
docker compose exec client ping api-service
```

Both hostnames resolve to the same services due to network aliases.

#### Step 4: Test Load Balancing

Access the client application at http://localhost:8000 repeatedly and observe how requests are distributed among the API instances.

### Exercise 4: Real-World Microservices Networking

This exercise implements a complex microservices architecture with sophisticated networking.

#### Step 1: Examine the Network Architecture

```bash
cd ../exercise4
cat docker-compose.yml
```

Notice the network segmentation with gateway, service, and database networks.

#### Step 2: Start the Microservices

```bash
docker compose up -d
```

#### Step 3: Test the Gateway Pattern

The `gateway` service is the only one exposed to the host. It routes requests to internal services based on paths.

Access the application at http://localhost:8080/users and http://localhost:8080/products to see this in action.

#### Step 4: Test Network Isolation

```bash
docker compose exec gateway ping users-service
docker compose exec gateway ping products-service
docker compose exec users-service ping db-service
docker compose exec products-service ping users-service
```

Observe which services can communicate with each other based on the network configuration.

## Network Inspection and Troubleshooting

### Inspecting Networks

To list all networks:
```bash
docker network ls
```

To inspect a specific network:
```bash
docker network inspect exercise1_app-network
```

### Troubleshooting Tools

To check connectivity between containers:
```bash
docker compose exec <service> ping <target-service>
```

To trace network routes:
```bash
docker compose exec <service> traceroute <target-service>
```

To examine network interfaces:
```bash
docker compose exec <service> ip addr
```

## Cleanup

To clean up the resources created in each exercise:
```bash
# From the exercise directory
docker compose down

# To also remove volumes
docker compose down -v
```

## Best Practices for Docker Compose Networking

1. **Use Custom Networks**: Always define custom networks for better control and isolation
2. **Network Segmentation**: Create separate networks for different application tiers
3. **Limit Exposure**: Only expose necessary ports to the host
4. **Use Internal Networks**: Keep databases and sensitive services on internal networks
5. **Consider Network Drivers**: Choose the appropriate network driver for your use case
6. **DNS Resolution**: Use container names for service discovery
7. **Multiple Networks**: Connect services to multiple networks when necessary
8. **Network Aliases**: Use aliases for service discovery flexibility

## Conclusion

This lab has demonstrated advanced networking configurations in Docker Compose, from basic service discovery to complex multi-tier architectures. These skills are essential for building robust, secure, and scalable containerized applications. 