#!/bin/bash

# Script to analyze Docker images in Linux

# Check if image name is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [image_name]"
    echo "Example: $0 layers-demo:unoptimized"
    exit 1
fi

IMAGE_NAME=$1

echo "Analyzing Docker image: $IMAGE_NAME"
echo "=========================================="
echo ""

# Standard Docker commands for layer analysis
echo "Running docker history:"
docker history $IMAGE_NAME

echo ""
echo "Running docker image inspect (size information):"
docker image inspect $IMAGE_NAME | grep -E 'Size|Id|Created'

echo ""
echo "To analyze with dive tool, run:"
echo "docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest $IMAGE_NAME"

# Total image size
echo ""
echo "Image size summary:"
docker images $IMAGE_NAME --format "{{.Repository}}:{{.Tag}} - {{.Size}}" 