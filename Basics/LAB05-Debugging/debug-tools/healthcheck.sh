#!/bin/bash
# Container health check script

# Check if container name is provided
CONTAINER=$1

if [ -z "$CONTAINER" ]; then
  echo "Usage: $0 <container_name>"
  echo "Example: $0 my-nginx"
  exit 1
fi

# Check if container exists
if ! docker ps -a --format "{{.Names}}" | grep -q "^$CONTAINER$"; then
  echo "Error: Container '$CONTAINER' does not exist"
  exit 1
fi

echo "================================"
echo "CONTAINER HEALTH CHECK: $CONTAINER"
echo "================================"

# Basic container info
echo -e "\n== BASIC INFO =="
echo "Status: $(docker inspect -f '{{.State.Status}}' $CONTAINER)"
echo "Running: $(docker inspect -f '{{.State.Running}}' $CONTAINER)"
echo "Started At: $(docker inspect -f '{{.State.StartedAt}}' $CONTAINER)"
echo "Exit Code: $(docker inspect -f '{{.State.ExitCode}}' $CONTAINER)"

# Health check status if available
HEALTH=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}No health check defined{{end}}' $CONTAINER)
echo -e "\n== HEALTH STATUS =="
echo "Health: $HEALTH"

# If health check exists, show the last few results
if [ "$HEALTH" != "No health check defined" ]; then
  echo -e "\nLast 3 health check results:"
  docker inspect -f '{{range $i, $e := .State.Health.Log}}{{if lt $i 3}}{{$e.Start}}: {{$e.ExitCode}} - {{$e.Output}}{{println}}{{end}}{{end}}' $CONTAINER
fi

# Network info
echo -e "\n== NETWORK INFO =="
docker inspect -f '{{range $net, $conf := .NetworkSettings.Networks}}Network: {{$net}}, IP: {{$conf.IPAddress}}{{println}}{{end}}' $CONTAINER

# Resource usage
echo -e "\n== RESOURCE USAGE =="
docker stats --no-stream $CONTAINER

# Environment variables
echo -e "\n== ENVIRONMENT VARIABLES =="
docker inspect -f '{{range .Config.Env}}{{.}}{{println}}{{end}}' $CONTAINER

# Mounts
echo -e "\n== VOLUME MOUNTS =="
docker inspect -f '{{range .Mounts}}Type: {{.Type}}, Source: {{.Source}}, Destination: {{.Destination}}{{println}}{{end}}' $CONTAINER

# Last log entries
echo -e "\n== LOGS (last 10 lines) =="
docker logs --tail 10 $CONTAINER

echo -e "\n== END OF HEALTH CHECK ==" 