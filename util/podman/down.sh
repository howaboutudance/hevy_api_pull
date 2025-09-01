#!/usr/bin/env bash

# A podman development environment for hevy_api_pull
# This script tears down the podman containers for the development
# environment individually

# stop and remove the mongodb container
podman stop mongodb_server
podman rm mongodb_server

# remove the mongodb pod
podman pod rm mongodb_pod

# if `--remove-volumes` is passed
if [[ "$1" == "--remove-volumes" ]]; then
    # remove the mongodb volume
    podman volume rm mongodb_data
fi
