#!/bin/sh

# This script restores a backup to a Docker volume

# Check if backup file is provided
if [ -z "$1" ]; then
  echo "Error: No backup file provided"
  echo "Usage: $0 <backup_file>"
  exit 1
fi

# Backup file to restore
BACKUP_FILE="/backups/$1"

# Check if the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: Backup file not found: $BACKUP_FILE"
  echo "Available backups:"
  ls -la /backups
  exit 1
fi

echo "Restoring from backup: ${BACKUP_FILE}..."

# Clean any existing data in the target volume
echo "Cleaning target volume..."
rm -rf /target/*

# Restore the backup using tar
echo "Extracting backup data to volume..."
tar -xzvf $BACKUP_FILE -C /target

echo "Restore completed successfully!"
ls -la /target 