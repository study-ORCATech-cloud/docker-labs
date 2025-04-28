#!/bin/bash
# Container resource monitoring script

# Default interval is 5 seconds
INTERVAL=${1:-5}

echo "Docker Container Resource Monitor"
echo "Press Ctrl+C to exit"
echo "-----------------------------------"

while true; do 
  echo ""
  echo "===== $(date) ====="
  
  # Get container stats in non-streaming mode
  docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}"
  
  # Show containers that have recently exited
  EXITED=$(docker ps -f "status=exited" --format "{{.Names}} (exited: {{.Status}})" | head -n 5)
  if [ ! -z "$EXITED" ]; then
    echo ""
    echo "Recently exited containers:"
    echo "$EXITED"
  fi
  
  # Sleep for the specified interval
  sleep $INTERVAL
done 