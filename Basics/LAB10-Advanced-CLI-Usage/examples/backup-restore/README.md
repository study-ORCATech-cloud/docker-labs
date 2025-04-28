# Docker CLI-Based Backup and Restore

This guide covers techniques for backing up and restoring Docker containers, images, volumes, and configuration using CLI commands.

## Overview

Effective backup and restore strategies are essential for:
- Disaster recovery
- Data migration between environments
- Version control of container state
- System upgrades
- Testing and development

## Container State Backup

### Exporting Running Containers

```bash
# Create a snapshot of a running container as a new image
docker commit my-container my-container-snapshot

# Export a container to a tarball (includes filesystem only, not volumes)
docker export my-container > my-container-backup.tar

# Import a container tarball as a new image
cat my-container-backup.tar | docker import - my-restored-image

# Run a new container from the snapshot
docker run -d --name my-restored-container my-container-snapshot
```

### Container Configuration Backup

```bash
# Back up container configuration (inspect output)
docker inspect my-container > my-container-config.json

# Extract specific configuration elements
docker inspect --format='{{json .HostConfig}}' my-container > hostconfig.json
docker inspect --format='{{json .Config}}' my-container > config.json

# Recreate container with similar configuration
docker run --name new-container $(cat hostconfig-params.txt) my-image
```

## Volume Data Backup

### Direct Volume Backup

```bash
# List volumes to identify what to back up
docker volume ls

# Back up a named volume using an intermediate container
docker run --rm -v my-volume:/source:ro -v $(pwd):/backup alpine tar -czf /backup/my-volume-backup.tar.gz -C /source .

# Restore a volume from backup
docker run --rm -v my-volume:/target -v $(pwd):/backup alpine sh -c "cd /target && tar -xzf /backup/my-volume-backup.tar.gz"
```

### Volume Backup with Data Verification

```bash
# Back up with checksums
docker run --rm -v my-volume:/source:ro -v $(pwd):/backup alpine sh -c "cd /source && find . -type f | xargs md5sum > /backup/checksums.md5 && tar -czf /backup/my-volume-backup.tar.gz ."

# Verify restored data
docker run --rm -v my-volume:/target -v $(pwd):/backup alpine sh -c "cd /target && md5sum -c /backup/checksums.md5"
```

### Backing Up Bind Mounts

```bash
# For bind mounts, you can directly back up the host directory
tar -czf nginx-html-backup.tar.gz -C /path/to/nginx/html .

# Restore to the host directory
mkdir -p /path/to/nginx/html
tar -xzf nginx-html-backup.tar.gz -C /path/to/nginx/html
```

## Docker Image Backup

### Saving and Loading Images

```bash
# Save one or more images to a tarball
docker save -o my-images.tar image1:tag1 image2:tag2

# Load images from a tarball
docker load -i my-images.tar

# Save all local images (be careful, this could be large)
docker save -o all-images.tar $(docker images -q)
```

### Selective Image Backup

```bash
# Save images matching a filter
docker save -o production-images.tar $(docker images --filter=reference='myapp:*' -q)

# Save images with labels
docker save -o backend-images.tar $(docker images --filter=label=component=backend -q)
```

## Network Configuration Backup

```bash
# Back up network configuration
docker network ls --format "{{.Name}}" | xargs -I{} sh -c 'docker network inspect {} > network-{}.json'

# Recreate a custom network from backup
network_name=$(jq -r '.[0].Name' network-my-network.json)
subnet=$(jq -r '.[0].IPAM.Config[0].Subnet' network-my-network.json)
gateway=$(jq -r '.[0].IPAM.Config[0].Gateway' network-my-network.json)

docker network create --subnet=$subnet --gateway=$gateway $network_name
```

## Complete System Backup

### Container Environment Backup

```bash
# Create a backup script for a complete environment
cat > docker-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="docker-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR/{containers,volumes,networks,images}

# Backup running containers
docker ps -a --format "{{.Names}}" > $BACKUP_DIR/container-names.txt
for container in $(cat $BACKUP_DIR/container-names.txt); do
  docker inspect $container > $BACKUP_DIR/containers/$container.json
done

# Backup volumes
docker volume ls --format "{{.Name}}" > $BACKUP_DIR/volume-names.txt
for volume in $(cat $BACKUP_DIR/volume-names.txt); do
  docker run --rm -v $volume:/source:ro -v $(pwd)/$BACKUP_DIR/volumes:/backup alpine tar -czf /backup/$volume.tar.gz -C /source .
done

# Backup networks
docker network ls --format "{{.Name}}" | grep -v "bridge\|host\|none" > $BACKUP_DIR/network-names.txt
for network in $(cat $BACKUP_DIR/network-names.txt); do
  docker network inspect $network > $BACKUP_DIR/networks/$network.json
done

# Backup images (only custom images, not pulled from Docker Hub)
docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "docker.io" > $BACKUP_DIR/image-names.txt
docker save -o $BACKUP_DIR/images/custom-images.tar $(cat $BACKUP_DIR/image-names.txt)

# Create a final tarball
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup completed: $BACKUP_DIR.tar.gz"
EOF
chmod +x docker-backup.sh
```

### Container Environment Restore

```bash
# Create a restore script
cat > docker-restore.sh << 'EOF'
#!/bin/bash
if [ $# -ne 1 ]; then
  echo "Usage: $0 backup-file.tar.gz"
  exit 1
fi

BACKUP_FILE=$1
TEMP_DIR="docker-restore-temp"

# Extract backup
mkdir -p $TEMP_DIR
tar -xzf $BACKUP_FILE -C $TEMP_DIR
BACKUP_DIR=$(ls $TEMP_DIR)

# Restore images
docker load -i $TEMP_DIR/$BACKUP_DIR/images/custom-images.tar

# Restore networks
for network_file in $TEMP_DIR/$BACKUP_DIR/networks/*.json; do
  network_name=$(jq -r '.[0].Name' $network_file)
  subnet=$(jq -r '.[0].IPAM.Config[0].Subnet' $network_file)
  gateway=$(jq -r '.[0].IPAM.Config[0].Gateway' $network_file)
  
  # Create network if it doesn't exist
  if ! docker network inspect $network_name > /dev/null 2>&1; then
    docker network create --subnet=$subnet --gateway=$gateway $network_name
  fi
done

# Restore volumes
for volume in $(cat $TEMP_DIR/$BACKUP_DIR/volume-names.txt); do
  # Create volume if it doesn't exist
  if ! docker volume inspect $volume > /dev/null 2>&1; then
    docker volume create $volume
  fi
  
  # Restore data
  docker run --rm -v $volume:/target -v $(pwd)/$TEMP_DIR/$BACKUP_DIR/volumes:/backup alpine sh -c "cd /target && tar -xzf /backup/$volume.tar.gz"
done

# Restore containers (this is complex and may need customization)
for container_file in $TEMP_DIR/$BACKUP_DIR/containers/*.json; do
  container_name=$(jq -r '.[0].Name' $container_file | sed 's/^\///')
  image=$(jq -r '.[0].Config.Image' $container_file)
  
  # Extract and build run command (simplified, may need customizing)
  ports=$(jq -r '.[0].HostConfig.PortBindings | to_entries[] | "-p " + (.value[0].HostPort) + ":" + (.key | split("/")[0])' $container_file | tr '\n' ' ')
  volumes=$(jq -r '.[0].HostConfig.Binds[]? | "-v " + .' $container_file | tr '\n' ' ')
  env=$(jq -r '.[0].Config.Env[] | "--env " + .' $container_file | tr '\n' ' ')
  network=$(jq -r '.[0].HostConfig.NetworkMode' $container_file)
  
  # Run container
  cmd="docker run -d --name $container_name $ports $volumes $env --network $network $image"
  echo "Running: $cmd"
  eval $cmd
done

# Cleanup
rm -rf $TEMP_DIR
echo "Restore completed"
EOF
chmod +x docker-restore.sh
```

## Scheduled Backups

### Setting Up Automated Backups

```bash
# Create a backup directory
mkdir -p /var/backups/docker

# Set up a daily backup cron job
echo "0 2 * * * /path/to/docker-backup.sh > /var/log/docker-backup.log 2>&1" | crontab -

# Implement backup rotation (keep last 7 days)
cat > /usr/local/bin/rotate-backups.sh << 'EOF'
#!/bin/bash
find /var/backups/docker -name "docker-backup-*.tar.gz" -type f -mtime +7 -delete
EOF
chmod +x /usr/local/bin/rotate-backups.sh
echo "0 3 * * * /usr/local/bin/rotate-backups.sh" | crontab -
```

## Remote Backup and Restore

### Backup to Remote Storage

```bash
# Back up to a remote server using SSH
docker save myapp:latest | ssh user@backup-server "cat > /backups/myapp-$(date +%Y%m%d).tar"

# Back up volume to remote storage
docker run --rm -v my-volume:/source:ro alpine tar -cz -C /source . | ssh user@backup-server "cat > /backups/my-volume-$(date +%Y%m%d).tar.gz"
```

### Restore from Remote Storage

```bash
# Restore image from remote storage
ssh user@backup-server "cat /backups/myapp-20230101.tar" | docker load

# Restore volume from remote storage
docker volume create my-volume
ssh user@backup-server "cat /backups/my-volume-20230101.tar.gz" | docker run --rm -i -v my-volume:/target alpine sh -c "cd /target && tar -xz"
```

## Database Container Backup

### PostgreSQL Backup

```bash
# Back up PostgreSQL database
docker exec postgres pg_dump -U postgres mydb > mydb-backup.sql

# Restore PostgreSQL database
docker exec -i postgres psql -U postgres mydb < mydb-backup.sql
```

### MySQL Backup

```bash
# Back up MySQL database
docker exec mysql mysqldump -u root -p mydb > mydb-backup.sql

# Restore MySQL database
docker exec -i mysql mysql -u root -p mydb < mydb-backup.sql
```

## Best Practices

1. **Test Your Backups:**
   - Regularly test restore procedures
   - Verify data integrity after restoration

2. **Automate Backup Processes:**
   - Schedule regular backups
   - Implement backup rotation

3. **Document Backup and Restore Procedures:**
   - Create detailed documentation
   - Maintain a backup inventory

4. **Secure Your Backups:**
   - Encrypt sensitive data
   - Store backups in secure locations

5. **Monitor Backup Success/Failure:**
   - Implement backup success notifications
   - Alert on backup failures

## TODO Tasks

1. Implement container state backup:
   - Create scripts to commit and export containers
   - Test container restoration from backups
   - Document the container state backup process

2. Set up volume data backup:
   - Create scripts for backing up named volumes
   - Implement incremental backup capabilities
   - Test volume restoration

3. Implement image backup:
   - Create a script to save important images
   - Set up image versioning
   - Test image restoration

4. Create a complete environment backup:
   - Develop a script for backing up all containers, volumes, and networks
   - Implement data verification
   - Test full environment restoration

5. Set up scheduled backups:
   - Configure cron jobs for automated backups
   - Implement backup rotation
   - Set up backup success/failure notifications

6. Implement remote backup:
   - Set up secure remote storage
   - Create scripts for transferring backups
   - Test remote restoration

7. Create database-specific backup procedures:
   - Implement backup scripts for different database types
   - Set up consistent state backups
   - Test database restoration

8. Develop a backup monitoring system:
   - Create a dashboard for backup status
   - Set up alerts for backup failures
   - Track backup size and timing trends

9. Implement backup encryption:
   - Set up backup encryption
   - Create secure key management
   - Test encrypted backup restoration

10. Document your backup strategy:
    - Create a comprehensive backup policy
    - Document all backup and restore procedures
    - Create a disaster recovery plan

## Additional Resources

- [Docker Export Command](https://docs.docker.com/engine/reference/commandline/export/)
- [Docker Save Command](https://docs.docker.com/engine/reference/commandline/save/)
- [Docker Volumes Documentation](https://docs.docker.com/storage/volumes/)
- [Docker Inspect Command](https://docs.docker.com/engine/reference/commandline/inspect/)
- [Data Backup Best Practices](https://www.docker.com/blog/how-to-backup-and-restore-docker-swarm/) 