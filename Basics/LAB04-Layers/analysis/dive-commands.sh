#!/bin/bash

# Script to analyze Docker images with dive tool

# Check if image names are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [image_name]"
    echo "Example: $0 layers-demo:unoptimized"
    exit 1
fi

IMAGE_NAME=$1

echo "Analyzing Docker image: $IMAGE_NAME"
echo "=========================================="
echo ""

# Run dive tool to analyze the image
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest $IMAGE_NAME

# Note: This script is a wrapper for the dive tool.
# You can also run docker history and docker image inspect:
# docker history $IMAGE_NAME
# docker image inspect $IMAGE_NAME 