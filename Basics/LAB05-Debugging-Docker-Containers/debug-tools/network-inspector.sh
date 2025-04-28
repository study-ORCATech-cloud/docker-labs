#!/bin/bash
# Docker network inspector script

# Usage information
show_usage() {
  echo "Docker Network Inspector"
  echo "Usage: $0 [container_name]"
  echo ""
  echo "If container_name is provided, will focus on that container's network."
  echo "Otherwise, will show all networks and containers."
}

# Handle arguments
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  show_usage
  exit 0
fi

CONTAINER=$1

# List all Docker networks
show_networks() {
  echo "=== Docker Networks ==="
  docker network ls
  echo ""
}

# Show detailed info for a specific network
inspect_network() {
  local network=$1
  echo "=== Network Details: $network ==="
  docker network inspect $network | grep -E 'Name|Driver|Subnet|Gateway|Container'
  echo ""
}

# Show networking details for a specific container
inspect_container_network() {
  local container=$1
  echo "=== Container Network Info: $container ==="
  echo "IP Address(es):"
  docker inspect -f '{{range $net, $conf := .NetworkSettings.Networks}}Network: {{$net}}, IP: {{$conf.IPAddress}}, Gateway: {{$conf.Gateway}}{{println}}{{end}}' $container
  
  echo "Exposed Ports:"
  docker inspect -f '{{range $port, $conf := .NetworkSettings.Ports}}{{$port}} -> {{$conf}}{{println}}{{end}}' $container
  
  echo "Connected Networks:"
  docker inspect -f '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}}{{println}}{{end}}' $container
  echo ""
}

# Attempt to run basic network tests in a container
test_container_connectivity() {
  local container=$1
  echo "=== Connectivity Tests for $container ==="
  
  # Check if the container has ping
  if docker exec $container which ping &>/dev/null; then
    echo "Testing connection to Google DNS (8.8.8.8):"
    docker exec $container ping -c 2 8.8.8.8
    
    echo "Testing DNS resolution (google.com):"
    docker exec $container ping -c 2 google.com
  else
    echo "Ping not available in container"
  fi
  
  # Check if the container has curl
  if docker exec $container which curl &>/dev/null; then
    echo "Testing HTTP connectivity (httpbin.org):"
    docker exec $container curl -s -o /dev/null -w "Status code: %{http_code}\n" httpbin.org/get
  else
    echo "Curl not available in container"
  fi
  
  echo ""
}

# Main script execution
echo "DOCKER NETWORK INSPECTOR"
echo "========================"
echo ""

# Show all networks
show_networks

# If a container is specified, focus on that container
if [ ! -z "$CONTAINER" ]; then
  # Check if container exists
  if ! docker ps -a --format "{{.Names}}" | grep -q "^$CONTAINER$"; then
    echo "Error: Container '$CONTAINER' does not exist"
    exit 1
  fi
  
  # Get networks this container is connected to
  NETWORKS=$(docker inspect -f '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}} {{end}}' $CONTAINER)
  
  # Inspect each network this container is connected to
  for network in $NETWORKS; do
    inspect_network $network
  done
  
  # Show container network details
  inspect_container_network $CONTAINER
  
  # Check if container is running before connectivity tests
  if docker inspect -f '{{.State.Running}}' $CONTAINER | grep -q "true"; then
    test_container_connectivity $CONTAINER
  else
    echo "Container is not running, skipping connectivity tests"
  fi
else
  echo "No container specified. Showing summary of all networks."
  echo ""
  
  # For each network, show the connected containers
  for network in $(docker network ls --format "{{.Name}}"); do
    echo "=== Containers in network: $network ==="
    docker network inspect $network -f '{{range .Containers}}{{.Name}} ({{.IPv4Address}}){{println}}{{end}}' | sort
    echo ""
  done
fi

echo "Network inspection complete" 