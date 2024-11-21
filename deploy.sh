#!/bin/bash

echo "Pulling new version"
git pull
echo "Build new docker"
sudo docker build -t cryptofinder .
echo "Deploy"
CONTAINER_ID=$(sudo docker run -d -p 10000:80 cryptofinder)
echo "Docker ID $CONTAINER_ID"
sleep 2
docker logs $CONTAINER_ID
