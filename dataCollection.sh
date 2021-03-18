#!/usr/bin/env bash

cwd=$PWD
# Set VOLUMENAME
VOLUMENAME="dataCollected"

# Create docker volume
docker volume create $VOLUMENAME

# Build and run docker volume, then get the container ID of the last ran container
docker build . -t code
docker run -v $VOLUMENAME:/app code -u $1 -t $2 -o $3 

CONTAINERID="$(docker ps -q -n 1)"

# Copy volume data to the CWD
docker container cp $CONTAINERID:/app/$3 $cwd

# Remove created docker containers and volumes after the container has been stopped
echo "Stopping docker container" $CONTAINERID
docker stop $CONTAINERID

echo "Deleting container with ID:" $CONTAINERID
docker rm $CONTAINERID

echo "Deleting volume with NAME:" $VOLUMENAME
docker volume rm $VOLUMENAME

echo "Deleting ALL DOCKER CONTAINERS AND VOLUMES"
docker system prune -a --volumes

echo "Data collection created and stored in ${cwd}"
