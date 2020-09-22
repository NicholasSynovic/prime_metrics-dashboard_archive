#!/usr/bin/env bash

# Get cwd
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create docker volume
docker volume create metrics

# Build and run docker volume, then get the container ID of the last ran container
docker build -t commits .
docker run -v metrics:/metrics commits $1 $2

CONTAINERID="$(docker ps -q -n 1)"

echo $CONTAINERID

# Copy volume data to the cwd
# TODO: Fix this so that it actually copies data
docker cp $CONTAINERID:/metrics $DIR

# Remove created docker containers and volumes after the container has been stopped
echo "Stopping docker container" $CONTAINERID
docker stop $CONTAINERID

# TODO: Create code that deletes the container based off of CONTAINERID
# TODO: Create code that deletes the volume based off of VOLUMENAME

echo "Deleting ALL DOCKER CONTAINERS AND VOLUMES"
docker system prune -a --volumes

echo "Metrics created and stored in" $DIR"/metrics"
