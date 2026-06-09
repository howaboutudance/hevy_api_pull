#!/usr/bin/env bash
# Builds the AWS Lambda deployment package for the webhook component.
#
# Installs the Lambda runtime dependencies (built for the Lambda
# python3.12 x86_64 runtime) and copies the application source and
# configuration into terraform/build/package, which Terraform then zips.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TF_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(dirname "$TF_DIR")"
PACKAGE_DIR="$TF_DIR/build/package"

LAMBDA_PYTHON_VERSION="${LAMBDA_PYTHON_VERSION:-3.12}"

rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

python3 -m pip install \
  --quiet \
  --target "$PACKAGE_DIR" \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version "$LAMBDA_PYTHON_VERSION" \
  --only-binary=:all: \
  --requirement "$TF_DIR/lambda/requirements.txt"

cp -r "$REPO_ROOT/src/app" "$PACKAGE_DIR/app"
cp -r "$REPO_ROOT/config" "$PACKAGE_DIR/config"

# remove caches and secrets so the archive is stable and clean
find "$PACKAGE_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
rm -f "$PACKAGE_DIR"/config/.secrets.yaml

echo "Lambda package built at $PACKAGE_DIR"
