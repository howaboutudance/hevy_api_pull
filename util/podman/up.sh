#!/usr/bin/env bash

# A podman development environment for hevy_api_pull
# This script sets up and starts the podman containers for the development
# environment individually

# create a network for hevy_api_pull if doesn't exist
podman network inspect hevy_api_pull || podman network create hevy_api_pull

# create a pod for mongodb and expose port 27017
podman pod create --name mongodb_pod --network hevy_api_pull -p 27017:27017

# create a volume for use with mongodb
podman volume create mongodb_data

# run a container for mongodb
podman run -d --name mongodb_server --pod mongodb_pod \
    -e MONGODB_INITDB_ROOT_USERNAME="admin" \
    -e MONGODB_INITDB_ROOT_PASSWORD=${MONGODB_PASSWORD} \
    -v mongodb_data:/data/db \
     mongodb/mongodb-community-server