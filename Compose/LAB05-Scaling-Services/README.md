# LAB05: Scaling Services with Docker Compose

This lab demonstrates how to scale services using Docker Compose for handling increased load and providing high availability.

## Learning Objectives

- Configure services for horizontal scaling in Docker Compose
- Implement and use the `--scale` flag with Docker Compose
- Configure a load balancer to distribute traffic across container replicas
- Understand how Docker's internal DNS handles service discovery
- Monitor and manage scaled container instances
- Implement basic auto-scaling for Docker Compose services

## Prerequisites

- Docker Engine installed
- Docker Compose v2 installed
- Basic understanding of Docker containers and Docker Compose
- Familiarity with YAML syntax
- Completion of previous labs recommended

## Important Instructions

This lab is designed for hands-on learning. You are expected to:
- Implement Docker Compose configurations yourself
- Follow the TODOs in the provided YAML files
- Test scaling with different numbers of replicas
- Document your findings about load balancing and scaling behavior

## Lab Environment

In this lab, you'll build a scalable application architecture consisting of:

1. **Web Application**: A Python Flask service that can be scaled horizontally
2. **Redis Database**: A centralized data store for maintaining shared state
3. **Nginx Load Balancer**: Distributes traffic across web application replicas

## Project Structure

```
LAB05-ScalingServices/
├── docker-compose.yml      # Main configuration file with TODOs
├── web/                    # Web application service
│   ├── Dockerfile          # Container definition for web service
│   ├── app.py              # Python Flask application
│   └── requirements.txt    # Python dependencies
├── nginx/                  # Load balancer configuration
│   └── nginx.conf          # Nginx configuration with TODOs
└── autoscale.py            # Optional auto-scaling script
```

## Lab Exercises

### Exercise 1: Configure Scalable Services

In this exercise, you'll prepare your Docker Compose configuration for scaling:

1. Review the `docker-compose.yml` file and identify the TODOs
2. Configure the web service to support horizontal scaling
3. Set up the Redis service for centralized data storage
4. Configure the Nginx service as a load balancer

### Exercise 2: Scale Services Manually

Learn how to scale services using Docker Compose commands:

1. Start the application with the default configuration
2. Scale the web service to multiple instances
3. Observe how Docker Compose creates and manages the new containers
4. Test the application to verify load balancing

### Exercise 3: Implement Advanced Load Balancing

Configure Nginx to effectively distribute traffic:

1. Review the `nginx.conf` file and identify the TODOs
2. Configure the upstream server group for load balancing
3. Implement proxy settings for proper request handling
4. Test the load balancer with multiple web service instances

### Exercise 4: Monitor Scaled Services

Learn how to monitor and manage scaled services:

1. Use Docker commands to view running containers
2. Monitor resource usage across container instances
3. Check container logs for multiple instances
4. Understand the relationship between service name and container instances

### Exercise 5: Implement Basic Auto-Scaling (Advanced)

For advanced users, implement a basic auto-scaling mechanism:

1. Review the `autoscale.py` script
2. Install the required dependencies
3. Configure the scaling thresholds
4. Run the script to automatically adjust service replicas based on CPU usage

## Getting Started

1. Review the main `docker-compose.yml` file and understand the architecture
2. Implement the TODOs in the configuration files
3. Start the application and test scaling features
4. Experiment with different numbers of replicas and observe behavior

## Docker Compose Scaling Commands

```bash
# Start the application with default configuration
docker-compose up -d

# Scale the web service to 5 instances
docker-compose up -d --scale web=5

# Check the running containers
docker-compose ps

# View logs from all web service instances
docker-compose logs web

# Scale down to 3 instances
docker-compose up -d --scale web=3

# Monitor container resource usage
docker stats
```

## Cleanup

When you're done with all exercises, you can clean up all resources with:

```bash
# Stop all containers and remove resources
docker-compose down -v

# Verify all containers are removed
docker-compose ps
```

## Best Practices

- Use named volumes for persistent data in scalable services
- Implement health checks for all services
- Configure resource limits to prevent container overconsumption
- Use load balancing algorithms appropriate for your traffic patterns
- Make services stateless where possible to simplify scaling
- Use central data stores for shared state between service instances

## Troubleshooting

- **Port conflicts**: When scaling services, avoid publishing the same port multiple times
- **Load balancer issues**: Check Nginx configuration and logs if requests aren't distributed
- **State inconsistencies**: Verify Redis connection is working across all instances
- **Performance problems**: Monitor container resources to identify bottlenecks

## Next Steps

After completing this lab, you'll be ready to move on to LAB06-ProductionCompose to learn about preparing your Docker Compose configurations for production environments. 