#!/bin/sh

# This script creates a backup of a Docker volume

# Check if volume name is provided
if [ -z "$1" ]; then
  echo "Error: No volume name provided"
  echo "Usage: $0 <volume_name>"
  exit 1
fi

# Volume to backup
VOLUME_NAME=$1

# Backup directory
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${VOLUME_NAME}_${TIMESTAMP}.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Creating backup of volume '${VOLUME_NAME}' to ${BACKUP_FILE}..."

# Create the backup using tar
tar -czvf $BACKUP_FILE -C /source .

echo "Backup completed successfully!"
echo "Backup saved to: ${BACKUP_FILE}"

# List all backups
echo "Available backups:"
ls -lh ${BACKUP_DIR} 