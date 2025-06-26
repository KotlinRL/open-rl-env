#!/bin/bash

# Fail immediately if any command fails
set -e

# Step 1: Navigate to the docker directory
cd "$(dirname "${BASH_SOURCE[0]}")/docker"
PROJECT_ROOT=$(pwd)

# Step 2: Set Docker image details
DOCKER_IMAGE_NAME="kotlinrl/open-rl-gymnasium-grpc-server"
DOCKER_TAG=${1:-latest}

# Step 3: Build the Docker Image
echo "Building Docker image..."
docker build -t "$DOCKER_IMAGE_NAME:$DOCKER_TAG" .
echo "Docker image built successfully: $DOCKER_IMAGE_NAME:$DOCKER_TAG"

# Step 4: Push Docker Image to Docker Hub
echo "Pushing Docker image to Docker Hub..."
docker push "$DOCKER_IMAGE_NAME:$DOCKER_TAG"
echo "Docker image pushed successfully to $DOCKER_IMAGE_NAME:$DOCKER_TAG"