#!/usr/bin/env bash

# Set VOLUMENAME
VOLUMENAME="commits"

# Get CWD
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create docker volume
docker volume create $VOLUMENAME

# Build and run docker volume, then get the container ID of the last ran container
docker build -t commits .
docker run -v $VOLUMENAME:/metrics commits $1 $2

CONTAINERID="$(docker ps -q -n 1)"

# Copy volume data to the CWD
docker container cp $CONTAINERID:/metrics $DIR

# Remove created docker containers and volumes after the container has been stopped
echo "Stopping docker container" $CONTAINERID
docker stop $CONTAINERID

echo "Deleting container with ID:" $CONTAINERID
docker rm $CONTAINERID

echo "Deleting volume with NAME:" $VOLUMENAME
docker volume rm $VOLUMENAME

# echo "Deleting ALL DOCKER CONTAINERS AND VOLUMES"
docker system prune -a --volumes

echo "Metrics created and stored in" $DIR"/metrics"
