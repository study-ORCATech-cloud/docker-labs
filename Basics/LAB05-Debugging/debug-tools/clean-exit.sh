#!/bin/bash
# Script to clean up exited containers

# Show total number of exited containers
EXITED_COUNT=$(docker ps -f "status=exited" -q | wc -l)
echo "Found $EXITED_COUNT exited containers"

if [ $EXITED_COUNT -eq 0 ]; then
  echo "No exited containers to clean up"
  exit 0
fi

# List exited containers
echo -e "\nExited containers:"
docker ps -f "status=exited" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Image}}"

# Confirm removal
read -p "Do you want to remove these containers? (y/n): " CONFIRM
if [[ $CONFIRM =~ ^[Yy]$ ]]; then
  echo "Removing exited containers..."
  
  # Remove all exited containers
  docker rm $(docker ps -f "status=exited" -q)
  
  echo "Cleanup complete!"
else
  echo "Cleanup cancelled"
fi

# Optional: also remove dangling images
read -p "Do you also want to remove dangling images? (y/n): " CONFIRM_IMAGES
if [[ $CONFIRM_IMAGES =~ ^[Yy]$ ]]; then
  echo "Removing dangling images..."
  
  # Remove dangling images
  docker image prune -f
  
  echo "Image cleanup complete!"
fi 