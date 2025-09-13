#!/bin/bash

set -e

echo "Pulling new version"
git pull

echo "Build new Docker image"
sudo docker build -t cryptofinder .

echo "Stop and remove existing container (if any)"
sudo docker stop cryptofinder 2>/dev/null || true
sudo docker rm cryptofinder 2>/dev/null || true

echo "Deploy new container"
CONTAINER_ID=$(sudo docker run -d --restart unless-stopped --name cryptofinder -p 10000:80 cryptofinder )
echo "Docker ID: $CONTAINER_ID (Name: cryptofinder)"

echo "Waiting for container logs..."
sleep 2
sudo docker logs cryptofinder
