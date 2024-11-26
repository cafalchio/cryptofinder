#!/bin/bash

set -e

echo "Pulling new version"
git pull

echo "Build new Docker image"
sudo docker build -t cryptofinder .

# Check port for existing container
PORT=$(sudo docker ps --format "table {{.Image}}{{.Ports}}" | grep cryptofinder | awk -F'->' '{print $1}' | awk -F':' '{print $2}')
if [[ $PORT -eq 10000 ]]; then
    PORT=10001
    REMOVE=cryptofinder10000
else
    PORT=10000
    REMOVE=cryptofinder10001
fi

echo "Deploy new container"
CONTAINER_ID=$(sudo docker run -d --name cryptofinder"$PORT" -p "$PORT":80 cryptofinder)
echo "Docker ID: $CONTAINER_ID (Name: cryptofinder$PORT)"

echo "Stop and remove existing container (if any)"
sudo docker stop "$REMOVE" 2>/dev/null || true
sudo docker rm "$REMOVE" 2>/dev/null || true

echo "Waiting for container logs..."
sleep 2
sudo docker logs cryptofinder"$PORT"
