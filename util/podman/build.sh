#!/usr/bin/env bash
# Build a container image using Podman
set -euo pipefail

IMAGE_NAME="hevy_api_pull"
VERSION=$(yq eval '.project.version' pyproject.toml)

podman build -t "${IMAGE_NAME}:${VERSION}" .
