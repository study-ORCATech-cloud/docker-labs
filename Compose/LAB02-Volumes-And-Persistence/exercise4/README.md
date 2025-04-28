# Exercise 4: Volume Backup and Restore

This exercise demonstrates how to back up and restore Docker volumes, which is essential for data management and disaster recovery.

## Overview

In this exercise, you will:
1. Configure Docker Compose for volume backup and restore operations
2. Create a backup of a PostgreSQL database volume
3. Restore the backup to a new volume
4. Learn best practices for volume data backup and recovery

## Files

- `backup.sh`: Shell script to create a volume backup
- `restore.sh`: Shell script to restore a volume from backup
- `/backups/`: Directory where backups are stored (mounted from host)

## Instructions

### Step 1: Configure the Docker Compose File

Before starting, add the backup service configuration to the `docker-compose.yml` file:

```yaml
# TODO: Configure the backup-service with:
# 1. The postgres_data volume mounted as read-only at /source
# 2. The local ./exercise4/backups directory mounted at /backups
```

This configuration will allow the backup service to access the PostgreSQL data volume without modifying it.

### Step 2: Create Data in the PostgreSQL Database

Before backing up data, ensure that the PostgreSQL database has some data:

```bash
# Make sure the PostgreSQL service is running
docker-compose up -d postgres-db

# Add some test data
docker-compose exec postgres-db psql -U dbuser -d persistence_demo -c "INSERT INTO notes (title, content) VALUES ('Backup Test', 'This note will be backed up and restored');"

# Verify the data exists
docker-compose exec postgres-db psql -U dbuser -d persistence_demo -c "SELECT * FROM notes;"
```

### Step 3: Create a Backup

```bash
# Use the backup-service container to run the backup script
docker-compose exec backup-service /backups/backup.sh postgres_data

# List the backups
docker-compose exec backup-service ls -lh /backups
```

### Step 4: Simulate Data Loss

Let's simulate a data loss scenario:

```bash
# Delete a note from the database
docker-compose exec postgres-db psql -U dbuser -d persistence_demo -c "DELETE FROM notes WHERE title = 'Backup Test';"

# Verify the note is gone
docker-compose exec postgres-db psql -U dbuser -d persistence_demo -c "SELECT * FROM notes WHERE title = 'Backup Test';"
```

### Step 5: Restore from Backup

To restore from a backup, we need to:
1. Stop the database service
2. Create a new restore service with the backup mounted
3. Run the restore script
4. Restart the database

```bash
# Stop the PostgreSQL service
docker-compose stop postgres-db

# Run a one-off container to restore the volume
# Replace BACKUP_FILENAME with the actual filename from step 2
docker run --rm -v lab02_postgres_data:/target -v $(pwd)/exercise4/backups:/backups alpine sh -c "sh /backups/restore.sh BACKUP_FILENAME"

# Start the PostgreSQL service again
docker-compose up -d postgres-db

# Verify the data has been restored
docker-compose exec postgres-db psql -U dbuser -d persistence_demo -c "SELECT * FROM notes WHERE title = 'Backup Test';"
```

### Step 6: Cleanup

When you're finished with this exercise, clean up the resources:

```bash
# Stop the containers
docker-compose stop postgres-db backup-service

# Remove the containers
docker-compose rm -f postgres-db backup-service

# If you want to remove the volume and delete all data
# docker volume rm lab02_postgres_data

# If you want to remove the backup files
# rm -rf exercise4/backups/*.tar.gz
```

## How Volume Backup Works

1. Mount the source volume to a temporary container
2. Use `tar` to compress the volume contents
3. Save the compressed archive to a host directory
4. For restoration, extract the archive to a target volume

## Best Practices for Production Environments

- Regularly schedule backups of important volumes
- Store backups in multiple locations (local and remote)
- Test restore procedures periodically
- Implement backup rotation (daily, weekly, monthly)
- Document backup and restore procedures
- Include volume backups in your disaster recovery plan

## Security Considerations

- Encrypt sensitive backups
- Control access to backup files
- Be careful with database dumps that might contain sensitive data
- Consider using database-specific backup tools for production environments

## Advanced Topics

- **Incremental Backups**: Only back up changed files
- **Point-in-Time Recovery**: Database WAL logs for time-specific recovery
- **Automated Backup Solutions**: Tools like restic, borg, or specialized Docker backup solutions
- **Remote Storage**: Pushing backups to S3, GCS, or other cloud storage
- **Docker Compose Extension**: Create a dedicated service for automated backups 