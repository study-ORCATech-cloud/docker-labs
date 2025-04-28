# Creating a Complete Docker CLI Workflow

This guide demonstrates how to integrate various Docker CLI techniques into a comprehensive workflow for container management.

## Overview

A complete Docker CLI workflow combines multiple aspects of Docker management:
- Image building and management
- Container deployment and orchestration
- Monitoring and observability
- Health checking and self-healing
- Logging and debugging
- Backup and disaster recovery
- Security scanning and enforcement
- Resource optimization

By integrating these components, you can create a robust container management system using just the Docker CLI.

## Setting Up the Workflow Environment

### Directory Structure

```
workflow/
├── config/                  # Configuration files
│   ├── app-config.env       # Application environment variables
│   ├── monitoring.env       # Monitoring configuration
│   └── networks.conf        # Network definitions
├── scripts/                 # Management scripts
│   ├── deploy.sh            # Deployment script
│   ├── monitor.sh           # Monitoring script
│   ├── backup.sh            # Backup script
│   ├── cleanup.sh           # Cleanup script
│   └── security-scan.sh     # Security scanning script
├── templates/               # Container templates
│   ├── web-service.tmpl     # Web service template
│   ├── db-service.tmpl      # Database service template
│   └── proxy-service.tmpl   # Proxy service template
└── README.md                # Documentation
```

### Configuration Management

Create standardized configuration files:

```bash
# app-config.env - Application configuration
APP_VERSION=1.2.3
DB_HOST=postgres
REDIS_HOST=redis
LOG_LEVEL=info

# networks.conf - Network definitions
APP_NETWORK=app-network
DB_NETWORK=db-network
PROXY_NETWORK=proxy-network
```

## Building a Deployment Script

Create a deployment script that manages the entire application lifecycle:

```bash
#!/bin/bash
# deploy.sh - Application deployment script

set -e

# Load configuration
source ./config/app-config.env
source ./config/networks.conf

# Functions
create_networks() {
    echo "Creating networks..."
    
    # Create app network if it doesn't exist
    if ! docker network inspect $APP_NETWORK >/dev/null 2>&1; then
        docker network create $APP_NETWORK
    fi
    
    # Create database network if it doesn't exist
    if ! docker network inspect $DB_NETWORK >/dev/null 2>&1; then
        docker network create $DB_NETWORK
    fi
    
    # Create proxy network if it doesn't exist
    if ! docker network inspect $PROXY_NETWORK >/dev/null 2>&1; then
        docker network create $PROXY_NETWORK
    fi
}

deploy_database() {
    echo "Deploying database..."
    
    # Deploy PostgreSQL database
    docker run -d --name postgres \
        --network $DB_NETWORK \
        -e POSTGRES_PASSWORD=mysecretpassword \
        -e POSTGRES_DB=appdb \
        -v postgres-data:/var/lib/postgresql/data \
        --health-cmd="pg_isready -U postgres" \
        --health-interval=5s \
        --health-timeout=3s \
        --health-retries=3 \
        --restart unless-stopped \
        postgres:13-alpine
    
    # Wait for database to be healthy
    echo "Waiting for database to be healthy..."
    until [ "$(docker inspect --format='{{.State.Health.Status}}' postgres)" = "healthy" ]; do
        sleep 2
    done
}

deploy_cache() {
    echo "Deploying cache..."
    
    # Deploy Redis cache
    docker run -d --name redis \
        --network $APP_NETWORK \
        --restart unless-stopped \
        redis:alpine
}

deploy_application() {
    echo "Deploying application services..."
    
    # Deploy backend API
    docker run -d --name api \
        --network $APP_NETWORK \
        --network $DB_NETWORK \
        -e DB_HOST=postgres \
        -e DB_PASSWORD=mysecretpassword \
        -e DB_NAME=appdb \
        -e REDIS_HOST=redis \
        --health-cmd="curl -f http://localhost:3000/health || exit 1" \
        --health-interval=10s \
        --health-timeout=3s \
        --health-retries=3 \
        --restart unless-stopped \
        myapp/api:${APP_VERSION}
    
    # Wait for API to be healthy
    echo "Waiting for API to be healthy..."
    until [ "$(docker inspect --format='{{.State.Health.Status}}' api)" = "healthy" ]; do
        sleep 2
    done
    
    # Deploy frontend replicas
    for i in {1..3}; do
        docker run -d --name frontend-$i \
            --network $APP_NETWORK \
            --network $PROXY_NETWORK \
            -e API_URL=http://api:3000 \
            --health-cmd="curl -f http://localhost:80/health || exit 1" \
            --health-interval=10s \
            --health-timeout=3s \
            --health-retries=3 \
            --restart unless-stopped \
            myapp/frontend:${APP_VERSION}
        
        # Wait for frontend to be healthy
        echo "Waiting for frontend-$i to be healthy..."
        until [ "$(docker inspect --format='{{.State.Health.Status}}' frontend-$i)" = "healthy" ]; do
            sleep 2
        done
    done
}

deploy_proxy() {
    echo "Deploying proxy..."
    
    # Create proxy configuration
    mkdir -p ./config/nginx
    cat > ./config/nginx/default.conf << EOF
upstream frontend {
    server frontend-1:80;
    server frontend-2:80;
    server frontend-3:80;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
    
    # Deploy Nginx proxy
    docker run -d --name proxy \
        --network $PROXY_NETWORK \
        -p 80:80 \
        -v $(pwd)/config/nginx:/etc/nginx/conf.d:ro \
        --restart unless-stopped \
        nginx:alpine
}

deploy_monitoring() {
    echo "Deploying monitoring..."
    
    # Deploy Prometheus for metrics
    docker run -d --name prometheus \
        --network $APP_NETWORK \
        -p 9090:9090 \
        -v $(pwd)/config/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
        --restart unless-stopped \
        prom/prometheus:latest
    
    # Deploy Grafana for dashboards
    docker run -d --name grafana \
        --network $APP_NETWORK \
        -p 3000:3000 \
        -v grafana-data:/var/lib/grafana \
        --restart unless-stopped \
        grafana/grafana:latest
}

# Main execution
echo "Deploying application version ${APP_VERSION}..."

create_networks
deploy_database
deploy_cache
deploy_application
deploy_proxy
deploy_monitoring

echo "Deployment completed successfully!"
```

## Creating a Monitoring Script

Build a comprehensive monitoring script:

```bash
#!/bin/bash
# monitor.sh - Application monitoring script

# Configuration
REPORT_DIR="./reports"
mkdir -p $REPORT_DIR

# Functions
check_health() {
    echo "Checking container health status..."
    
    # Check health status of all containers
    docker ps --format "{{.Names}}: {{.Status}}" | grep -v "health: starting"
    
    # List unhealthy containers
    UNHEALTHY=$(docker ps --filter health=unhealthy -q)
    if [ -n "$UNHEALTHY" ]; then
        echo "WARNING: Unhealthy containers detected!"
        docker ps --filter health=unhealthy --format "{{.Names}}"
        
        # Optionally, try to restart them
        for container in $UNHEALTHY; do
            echo "Restarting $container..."
            docker restart $container
        done
    fi
}

collect_resource_stats() {
    echo "Collecting resource usage statistics..."
    
    # Collect stats for all running containers
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" \
        > $REPORT_DIR/resource-stats-$(date +%Y%m%d-%H%M%S).txt
    
    # Identify high CPU containers
    HIGH_CPU=$(docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}" | grep -E "[7-9][0-9].[0-9]{2}%|100.00%" || true)
    if [ -n "$HIGH_CPU" ]; then
        echo "WARNING: High CPU usage detected!"
        echo "$HIGH_CPU"
    fi
    
    # Identify high memory containers
    HIGH_MEM=$(docker stats --no-stream --format "{{.Name}}: {{.MemPerc}}" | grep -E "[7-9][0-9].[0-9]{2}%|100.00%" || true)
    if [ -n "$HIGH_MEM" ]; then
        echo "WARNING: High memory usage detected!"
        echo "$HIGH_MEM"
    fi
}

check_disk_usage() {
    echo "Checking Docker disk usage..."
    
    # Check overall Docker disk usage
    docker system df -v > $REPORT_DIR/disk-usage-$(date +%Y%m%d-%H%M%S).txt
    
    # Check if we need to clean up
    TOTAL_USAGE=$(docker system df --format "{{.TotalCount}}" | head -1)
    if [ "$TOTAL_USAGE" -gt 100 ]; then
        echo "WARNING: High disk usage. Consider running cleanup script."
    fi
}

collect_logs() {
    echo "Collecting container logs..."
    
    # Collect recent logs from all containers
    for container in $(docker ps --format "{{.Names}}"); do
        docker logs --tail 100 $container > $REPORT_DIR/logs-$container-$(date +%Y%m%d-%H%M%S).txt
    done
    
    # Check for errors in logs
    ERROR_COUNT=$(grep -i "error\|exception\|fail" $REPORT_DIR/logs-* | wc -l)
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "WARNING: $ERROR_COUNT errors found in logs!"
    fi
}

# Main execution
echo "Starting monitoring at $(date)"

check_health
collect_resource_stats
check_disk_usage
collect_logs

echo "Monitoring completed at $(date)"
```

## Implementing a Backup Script

Create a backup script for data protection:

```bash
#!/bin/bash
# backup.sh - Application backup script

# Configuration
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Functions
backup_volumes() {
    echo "Backing up volumes..."
    
    # Back up PostgreSQL data
    docker run --rm \
        -v postgres-data:/source:ro \
        -v $BACKUP_DIR:/backup \
        alpine:latest \
        tar -czf /backup/postgres-data-$TIMESTAMP.tar.gz -C /source .
    
    # Back up Grafana data
    docker run --rm \
        -v grafana-data:/source:ro \
        -v $BACKUP_DIR:/backup \
        alpine:latest \
        tar -czf /backup/grafana-data-$TIMESTAMP.tar.gz -C /source .
}

backup_configs() {
    echo "Backing up configuration..."
    
    # Create a directory for configs
    mkdir -p $BACKUP_DIR/configs-$TIMESTAMP
    
    # Back up environment files
    cp ./config/*.env $BACKUP_DIR/configs-$TIMESTAMP/
    
    # Back up Nginx configuration
    cp -r ./config/nginx $BACKUP_DIR/configs-$TIMESTAMP/
    
    # Compress the configs
    tar -czf $BACKUP_DIR/configs-$TIMESTAMP.tar.gz -C $BACKUP_DIR configs-$TIMESTAMP
    rm -rf $BACKUP_DIR/configs-$TIMESTAMP
}

backup_container_state() {
    echo "Backing up container state..."
    
    # Create a directory for container state
    mkdir -p $BACKUP_DIR/containers-$TIMESTAMP
    
    # Back up container details
    docker ps -a --format "{{.Names}}" | while read container; do
        docker inspect $container > $BACKUP_DIR/containers-$TIMESTAMP/$container.json
    done
    
    # Compress the container state
    tar -czf $BACKUP_DIR/containers-$TIMESTAMP.tar.gz -C $BACKUP_DIR containers-$TIMESTAMP
    rm -rf $BACKUP_DIR/containers-$TIMESTAMP
}

rotate_backups() {
    echo "Rotating old backups..."
    
    # Keep only the last 7 days of backups
    find $BACKUP_DIR -type f -name "*.tar.gz" -mtime +7 -delete
}

# Main execution
echo "Starting backup at $(date)"

backup_volumes
backup_configs
backup_container_state
rotate_backups

echo "Backup completed at $(date)"
```

## Creating a Cleanup Script

Implement a cleanup script to manage resources:

```bash
#!/bin/bash
# cleanup.sh - Resource cleanup script

# Interactive mode flag
INTERACTIVE=true
if [ "$1" == "--force" ]; then
    INTERACTIVE=false
fi

# Functions
prompt_confirmation() {
    if [ "$INTERACTIVE" = true ]; then
        read -p "$1 (y/n): " response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
    return 0
}

cleanup_stopped_containers() {
    echo "Scanning for stopped containers..."
    STOPPED_COUNT=$(docker ps -a -f status=exited -q | wc -l)
    
    if [ "$STOPPED_COUNT" -gt 0 ]; then
        echo "Found $STOPPED_COUNT stopped containers."
        if prompt_confirmation "Remove all stopped containers?"; then
            docker container prune -f
            echo "Stopped containers removed."
        else
            echo "Skipping stopped container cleanup."
        fi
    else
        echo "No stopped containers found."
    fi
}

cleanup_unused_images() {
    echo "Scanning for unused images..."
    DANGLING_COUNT=$(docker images -f dangling=true -q | wc -l)
    
    if [ "$DANGLING_COUNT" -gt 0 ]; then
        echo "Found $DANGLING_COUNT dangling images."
        if prompt_confirmation "Remove dangling images?"; then
            docker image prune -f
            echo "Dangling images removed."
        else
            echo "Skipping dangling image cleanup."
        fi
    else
        echo "No dangling images found."
    fi
    
    UNUSED_COUNT=$(docker images -q | wc -l)
    if [ "$UNUSED_COUNT" -gt 20 ]; then  # Arbitrary threshold
        echo "You have $UNUSED_COUNT total images."
        if prompt_confirmation "Remove all unused images (not just dangling)?"; then
            docker image prune -a -f
            echo "Unused images removed."
        else
            echo "Skipping unused image cleanup."
        fi
    fi
}

cleanup_volumes() {
    echo "Scanning for unused volumes..."
    DANGLING_VOL_COUNT=$(docker volume ls -f dangling=true -q | wc -l)
    
    if [ "$DANGLING_VOL_COUNT" -gt 0 ]; then
        echo "Found $DANGLING_VOL_COUNT unused volumes."
        if prompt_confirmation "Remove unused volumes? WARNING: This will delete data!"; then
            docker volume prune -f
            echo "Unused volumes removed."
        else
            echo "Skipping volume cleanup."
        fi
    else
        echo "No unused volumes found."
    fi
}

cleanup_networks() {
    echo "Scanning for unused networks..."
    NETWORK_COUNT=$(docker network ls | grep -v "bridge\|host\|none" | wc -l)
    
    if [ "$NETWORK_COUNT" -gt 3 ]; then  # Arbitrary threshold
        echo "You have $NETWORK_COUNT custom networks."
        if prompt_confirmation "Remove unused networks?"; then
            docker network prune -f
            echo "Unused networks removed."
        else
            echo "Skipping network cleanup."
        fi
    else
        echo "No excess networks found."
    fi
}

full_system_prune() {
    echo "Considering full system prune..."
    
    if prompt_confirmation "Perform a full system prune? WARNING: This will remove all unused data!"; then
        if prompt_confirmation "Are you REALLY sure? This cannot be undone!"; then
            docker system prune -a -f --volumes
            echo "Full system prune completed."
        else
            echo "Full system prune cancelled."
        fi
    else
        echo "Skipping full system prune."
    fi
}

# Main execution
echo "Starting cleanup process at $(date)"

cleanup_stopped_containers
cleanup_unused_images
cleanup_volumes
cleanup_networks

# Only offer full prune in interactive mode
if [ "$INTERACTIVE" = true ]; then
    full_system_prune
fi

echo "Cleanup completed at $(date)"
```

## Implementing a Security Scanning Script

Create a security scanning script:

```bash
#!/bin/bash
# security-scan.sh - Security scanning script

# Configuration
REPORT_DIR="./security-reports"
mkdir -p $REPORT_DIR
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Functions
scan_images() {
    echo "Scanning images for vulnerabilities..."
    
    # Create a report file
    REPORT_FILE="$REPORT_DIR/vulnerability-scan-$TIMESTAMP.txt"
    echo "Docker Image Vulnerability Scan - $(date)" > $REPORT_FILE
    echo "=======================================" >> $REPORT_FILE
    
    # Scan all running containers
    for container in $(docker ps --format "{{.Names}}"); do
        image=$(docker inspect --format='{{.Config.Image}}' $container)
        echo "Scanning $container ($image)..." | tee -a $REPORT_FILE
        
        # Use Docker Scout if available
        if command -v docker-scout &> /dev/null; then
            docker scout cves $image >> $REPORT_FILE 2>&1
        # Fall back to Trivy if available
        elif command -v trivy &> /dev/null; then
            trivy image --no-progress $image >> $REPORT_FILE 2>&1
        else
            echo "No vulnerability scanner found. Install Docker Scout or Trivy." | tee -a $REPORT_FILE
        fi
        
        echo "----------------------------------------" >> $REPORT_FILE
    done
}

check_docker_bench() {
    echo "Running Docker Bench Security..."
    
    # Check if Docker Bench is available
    if [ -d "./docker-bench-security" ]; then
        cd ./docker-bench-security
        ./docker-bench-security.sh > "$REPORT_DIR/bench-security-$TIMESTAMP.txt"
        cd ..
    else
        echo "Docker Bench Security not found. Clone from https://github.com/docker/docker-bench-security"
    fi
}

check_image_best_practices() {
    echo "Checking image best practices..."
    
    REPORT_FILE="$REPORT_DIR/image-best-practices-$TIMESTAMP.txt"
    echo "Docker Image Best Practices - $(date)" > $REPORT_FILE
    echo "=======================================" >> $REPORT_FILE
    
    for image in $(docker image ls --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>"); do
        echo "Checking $image..." | tee -a $REPORT_FILE
        
        # Check for USER instruction (not running as root)
        USER_INSTRUCTION=$(docker inspect --format='{{.Config.User}}' $image)
        if [ -z "$USER_INSTRUCTION" ] || [ "$USER_INSTRUCTION" = "0" ] || [ "$USER_INSTRUCTION" = "root" ]; then
            echo "WARNING: Image $image runs as root" | tee -a $REPORT_FILE
        else
            echo "OK: Image runs as non-root user $USER_INSTRUCTION" | tee -a $REPORT_FILE
        fi
        
        # Check image size
        SIZE=$(docker inspect --format='{{.Size}}' $image)
        SIZE_MB=$((SIZE / 1000000))
        if [ $SIZE_MB -gt 500 ]; then
            echo "WARNING: Image size is large: $SIZE_MB MB" | tee -a $REPORT_FILE
        else
            echo "OK: Image size is $SIZE_MB MB" | tee -a $REPORT_FILE
        fi
        
        # Check number of layers
        LAYERS=$(docker inspect --format='{{len .RootFS.Layers}}' $image)
        if [ $LAYERS -gt 10 ]; then
            echo "WARNING: Image has many layers: $LAYERS" | tee -a $REPORT_FILE
        else
            echo "OK: Image has $LAYERS layers" | tee -a $REPORT_FILE
        fi
        
        echo "----------------------------------------" >> $REPORT_FILE
    done
}

# Main execution
echo "Starting security scan at $(date)"

scan_images
check_docker_bench
check_image_best_practices

echo "Security scan completed at $(date)"
```

## Creating a Rolling Update Script

Implement a rolling update script:

```bash
#!/bin/bash
# update.sh - Rolling update script

# Configuration
source ./config/app-config.env
NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new-version>"
    exit 1
fi

# Functions
update_api() {
    echo "Updating API service to version $NEW_VERSION..."
    
    # Pull new image
    docker pull myapp/api:$NEW_VERSION
    
    # Stop current container
    docker stop api
    docker rm api
    
    # Start new container
    docker run -d --name api \
        --network $APP_NETWORK \
        --network $DB_NETWORK \
        -e DB_HOST=postgres \
        -e DB_PASSWORD=mysecretpassword \
        -e DB_NAME=appdb \
        -e REDIS_HOST=redis \
        --health-cmd="curl -f http://localhost:3000/health || exit 1" \
        --health-interval=10s \
        --health-timeout=3s \
        --health-retries=3 \
        --restart unless-stopped \
        myapp/api:$NEW_VERSION
    
    # Wait for API to be healthy
    echo "Waiting for API to be healthy..."
    until [ "$(docker inspect --format='{{.State.Health.Status}}' api)" = "healthy" ]; do
        sleep 2
    done
}

update_frontends() {
    echo "Updating frontend services to version $NEW_VERSION..."
    
    # Pull new image
    docker pull myapp/frontend:$NEW_VERSION
    
    # Update each frontend one by one
    for i in {1..3}; do
        echo "Updating frontend-$i..."
        
        # Stop and remove current container
        docker stop frontend-$i
        docker rm frontend-$i
        
        # Start new container
        docker run -d --name frontend-$i \
            --network $APP_NETWORK \
            --network $PROXY_NETWORK \
            -e API_URL=http://api:3000 \
            --health-cmd="curl -f http://localhost:80/health || exit 1" \
            --health-interval=10s \
            --health-timeout=3s \
            --health-retries=3 \
            --restart unless-stopped \
            myapp/frontend:$NEW_VERSION
        
        # Wait for frontend to be healthy
        echo "Waiting for frontend-$i to be healthy..."
        until [ "$(docker inspect --format='{{.State.Health.Status}}' frontend-$i)" = "healthy" ]; do
            sleep 2
        done
    done
}

# Main execution
echo "Starting rolling update from version $APP_VERSION to $NEW_VERSION..."

update_api
update_frontends

# Update config file with new version
sed -i "s/APP_VERSION=.*/APP_VERSION=$NEW_VERSION/" ./config/app-config.env

echo "Update completed successfully!"
```

## Integrating into a Complete Workflow

Create a master script that manages the complete workflow:

```bash
#!/bin/bash
# workflow.sh - Master workflow script

# Set strict error handling
set -e

# Configuration
ACTION=$1
shift

# Functions
show_usage() {
    echo "Usage: $0 <action> [options]"
    echo
    echo "Actions:"
    echo "  deploy         Deploy the complete application"
    echo "  monitor        Monitor the application"
    echo "  backup         Backup data and configuration"
    echo "  cleanup        Clean up resources"
    echo "  security-scan  Perform security scanning"
    echo "  update <ver>   Perform a rolling update to <ver>"
    echo "  status         Show application status"
    echo "  logs <svc>     Show logs for a service"
    echo "  help           Show this help message"
    echo
    echo "Options:"
    echo "  --force        Skip confirmations (for cleanup)"
    echo "  --verbose      Show detailed output"
}

check_prerequisites() {
    echo "Checking prerequisites..."
    
    # Check Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker is running
    if ! docker info &> /dev/null; then
        echo "Error: Docker is not running"
        exit 1
    fi
    
    # Check required scripts exist
    for script in deploy.sh monitor.sh backup.sh cleanup.sh security-scan.sh update.sh; do
        if [ ! -f "./scripts/$script" ]; then
            echo "Error: Required script ./scripts/$script not found"
            exit 1
        fi
    done
}

show_status() {
    echo "Application Status:"
    echo "------------------"
    
    # Show running containers
    echo "Running Containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    # Show networks
    echo -e "\nNetworks:"
    docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}" | grep -v "bridge\|host\|none"
    
    # Show volumes
    echo -e "\nVolumes:"
    docker volume ls --format "table {{.Name}}\t{{.Driver}}\t{{.Mountpoint}}"
    
    # Show disk usage
    echo -e "\nDisk Usage:"
    docker system df
}

show_logs() {
    SERVICE=$1
    if [ -z "$SERVICE" ]; then
        echo "Error: No service specified for logs"
        echo "Usage: $0 logs <service-name>"
        exit 1
    fi
    
    # Check if service exists
    if ! docker ps --format "{{.Names}}" | grep -q "^$SERVICE$"; then
        echo "Error: Service $SERVICE not found"
        exit 1
    fi
    
    # Show logs
    docker logs --tail 100 -f $SERVICE
}

# Main execution
case "$ACTION" in
    deploy)
        check_prerequisites
        ./scripts/deploy.sh "$@"
        ;;
    monitor)
        check_prerequisites
        ./scripts/monitor.sh "$@"
        ;;
    backup)
        check_prerequisites
        ./scripts/backup.sh "$@"
        ;;
    cleanup)
        check_prerequisites
        ./scripts/cleanup.sh "$@"
        ;;
    security-scan)
        check_prerequisites
        ./scripts/security-scan.sh "$@"
        ;;
    update)
        check_prerequisites
        if [ -z "$1" ]; then
            echo "Error: No version specified for update"
            echo "Usage: $0 update <version>"
            exit 1
        fi
        ./scripts/update.sh "$1"
        ;;
    status)
        check_prerequisites
        show_status
        ;;
    logs)
        check_prerequisites
        show_logs "$1"
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "Error: Unknown action '$ACTION'"
        show_usage
        exit 1
        ;;
esac
```

## TODO Tasks

1. Create the complete workflow directory structure:
   - Set up the config, scripts, and templates directories
   - Initialize configuration files with default values
   - Create placeholder scripts for each function

2. Implement the deployment script:
   - Set up network management
   - Implement container dependency ordering
   - Add health checks for all components
   - Configure proper resource limits

3. Build the monitoring system:
   - Create resource usage monitoring
   - Implement health status checks
   - Set up automated recovery
   - Create log collection and analysis

4. Develop the backup solution:
   - Implement volume and data backup
   - Set up configuration backup
   - Create container state backup
   - Implement backup rotation

5. Create the security scanning system:
   - Implement vulnerability scanning
   - Set up Docker Bench Security checks
   - Create best practice compliance scanning
   - Add security reporting

6. Implement the update procedure:
   - Create rolling update mechanism
   - Implement health check verification
   - Add rollback capability
   - Configure update logging

7. Build the cleanup system:
   - Implement resource cleanup
   - Create image management
   - Set up volume maintenance
   - Add network cleanup

8. Integrate everything into the master workflow:
   - Create the main workflow script
   - Implement proper command-line interface
   - Add logging and status reporting
   - Create intuitive user experience

9. Test the complete workflow:
   - Verify each component works individually
   - Test the integrated workflow
   - Simulate failures and test recovery
   - Document lessons learned

10. Document your complete workflow:
    - Create detailed documentation
    - Add examples and use cases
    - Create troubleshooting guide
    - Provide customization instructions

## Additional Resources

- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Best Practices for Container Orchestration](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [Docker Backup and Restore](https://docs.docker.com/storage/volumes/#backup-restore-or-migrate-data-volumes)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/) 