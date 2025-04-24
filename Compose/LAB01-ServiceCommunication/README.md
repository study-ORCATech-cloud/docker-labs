# LAB01: Service Communication with Docker Compose

This lab demonstrates how to use Docker Compose to manage multiple containerized services and explore network communication between them. You'll learn how Docker's networking works and how to isolate services when needed.

## Lab Overview

In this lab, you will:
- Create and run multiple containerized services using Docker Compose
- Configure communication between services in a shared network
- Test service isolation by using separate networks
- Understand Docker's networking capabilities
- Learn techniques for connecting isolated services

## Learning Objectives

- Set up multiple services using Docker Compose
- Configure inter-service communication
- Understand Docker networking concepts
- Test network isolation between services
- Implement solutions for network connectivity challenges

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement Docker Compose configurations yourself
- Follow the TODOs in the provided YAML files
- Test service communication with various network configurations
- Document your findings about how Docker networking works

## Project Structure

```
LAB01-ServiceCommunication/
│
├── service1/                 # API service that calls service2
│   ├── Dockerfile           # Standard Dockerfile
│   ├── requirements.txt     # Python dependencies 
│   └── src/
│       └── main.py         # Flask app that makes requests to service2
│
├── service2/                 # Backend service
│   ├── chokomoko           # Custom-named Dockerfile
│   ├── requirements.txt     # Python dependencies
│   └── src/
│       └── main.py         # Flask app that provides responses
│
├── docker-compose.yaml       # TODO: Implement shared network configuration
└── docker-compose-isolated.yaml # TODO: Implement isolated networks configuration
```

---

## Part 1: Understanding the Services

### Service 1
- A simple Flask API running on port 5000
- Contains an endpoint `/getMessage` that makes HTTP requests to Service 2
- Depends on Service 2 being available

### Service 2
- A Flask API running on port 5001
- Provides a `/welcome` endpoint that returns a simple message
- Is referenced by the name "hibye" in the docker-compose configuration

## Part 2: Docker Compose Configuration with Shared Network

The default `docker-compose.yaml` needs to be completed with:
- **`service1`**: Configured to listen on port `5000` and connect to `service2`
- **`service2`** (named as `hibye`): Configured to listen on port `5001` and provide data
- Both services should be able to communicate with each other using service names as hostnames

### How Docker Compose Networking Works by Default:
- Docker Compose automatically creates a default network for all services
- Services can communicate with each other by referring to their service names as hostnames
- The `depends_on` parameter ensures `service2` starts before `service1`

## Part 3: Lab Exercises

### Exercise 1: Running Services on a Shared Network

1. **Complete the Docker Compose File**

   First, complete the TODOs in the `docker-compose.yaml` file to define both services properly.
   
   Key configurations to implement:
   - Build configurations for both services
   - Port mappings to access services from the host machine
   - Environment variables necessary for services to function
   - Service dependencies

2. **Build and Start Services**

   From the `LAB01-ServiceCommunication` directory, run:

   ```sh
   docker-compose up --build
   ```

   This command will:
   - Build both services using their respective Dockerfiles
   - Start the services in containers
   - Make them accessible on their defined ports

3. **Verify Services are Running**

   Check that both services are running:

   ```sh
   docker-compose ps
   ```

   You should see both services in the "Up" state.

4. **Test the Individual Services**

   Verify each service is responding correctly:

   ```sh
   # Test service1 liveness
   curl http://localhost:5000/liveness
   
   # Test service2 liveness
   curl http://localhost:5001/liveness
   
   # Test service2 welcome endpoint directly
   curl http://localhost:5001/welcome
   ```

5. **Test Inter-Service Communication**

   Now test if `service1` can successfully communicate with `service2`:

   ```sh
   curl http://localhost:5000/getMessage
   ```

   You should receive a response that includes the message from `service2`, indicating successful communication between the services.

6. **Explore Docker Networks**

   Examine the network that Docker Compose created:

   ```sh
   docker network ls
   # Find the network name that contains "lab01servicecommunication"
   
   # Inspect the network to see connected containers
   docker network inspect <network-name>
   ```

   You'll see both containers are connected to the same network.

### Exercise 2: Running Services on Isolated Networks

Now, let's see what happens when services are on separate networks and cannot communicate.

1. **Complete the Isolated Docker Compose File**

   Implement the TODOs in `docker-compose-isolated.yaml` to:
   - Configure both services similar to the default file
   - Connect each service to a different isolated network
   - Define both isolated networks

2. **Build and Start Services with Isolated Networks**

   Use the completed `docker-compose-isolated.yaml`:

   ```sh
   docker-compose -f docker-compose-isolated.yaml up --build
   ```

3. **Verify Services are Running**

   ```sh
   docker-compose -f docker-compose-isolated.yaml ps
   ```

4. **Test Inter-Service Communication (Expected to Fail)**

   When you try to access `service1`'s `/getMessage` endpoint, it should fail to reach `service2`:

   ```sh
   curl http://localhost:5000/getMessage
   ```

   You should receive an error response, as the services cannot communicate across their isolated networks.

5. **Explore Docker Networks**

   Examine the isolated networks:

   ```sh
   docker network ls
   # Find the network names for network1 and network2
   
   # Inspect the networks
   docker network inspect network1
   docker network inspect network2
   ```

   You'll see each service is connected only to its respective network.

### Exercise 3: Bridging the Gap (Advanced Exercise)

To enable communication between isolated services, you have several options:

1. **Connect a Service to Multiple Networks**

   Edit the `docker-compose-isolated.yaml` file to add `service1` to both networks:

   ```yaml
   service1:
     # Other settings remain the same
     networks:
       - network1
       - network2
   ```

   Then restart the services and test communication again.

2. **Use Docker's Network Connect Command**

   You can also connect an existing container to another network:

   ```sh
   # First get the container ID
   docker ps
   
   # Connect service1 to network2
   docker network connect network2 lab01servicecommunication-service1-1
   ```

   Try the `/getMessage` endpoint again after connecting the networks.

## Part 4: Real-World Applications

In production environments, service communication patterns like these are essential for:

- **Microservice Architecture**: Managing communication between independent services
- **Security Boundaries**: Creating network isolation between sensitive components
- **Multi-tier Applications**: Separating frontend, backend, and database layers
- **Service Discovery**: Enabling services to find and communicate with each other
- **Load Balancing**: Distributing traffic across multiple service instances

## Part 5: Additional Challenges

1. **Implement Service Discovery**: Modify the services to use Docker's DNS service discovery to locate each other dynamically.

2. **Add a Third Service**: Create a new service that aggregates data from both existing services and expose it on a different port.

3. **Implement a Bridge Service**: Create a dedicated bridge service that allows other services to communicate indirectly.

---

## Cleanup

When you're done with the lab, stop the running containers:

```sh
# For the default configuration
docker-compose down

# For the isolated networks configuration
docker-compose -f docker-compose-isolated.yaml down
```

To remove all created networks:

```sh
docker network prune
```

---

## Troubleshooting

### Cannot Access Services
- Check if the containers are running with `docker-compose ps`
- Verify that the ports are correctly mapped with `docker-compose port service1 5000`
- Check container logs with `docker-compose logs`

### Services Cannot Communicate
- Verify they are on the same network with `docker network inspect`
- Check if the service names are correctly specified in environment variables
- Ensure that the service dependency is configured properly 