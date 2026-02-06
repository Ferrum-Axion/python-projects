#!/usr/bin/env bash
set -e
VERSION="$(date +%Y%m%d%H%M%S)"
echo "Deploying version: $VERSION"

echo "Copying files..."
sudo cp -r site/* /var/www/devops-site/

echo "Validating nginx config..."
sudo nginx -t
sudo systemctl reload nginx

echo "Deployed $VERSION successfully"