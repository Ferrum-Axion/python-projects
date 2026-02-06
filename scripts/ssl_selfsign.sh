#!/usr/bin/env bash
set -e
echo "Generating self-signed SSL certificate..."
sudo mkdir -p /etc/nginx/ssl

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/selfsigned.key \
  -out /etc/nginx/ssl/selfsigned.crt \
  -subj "/CN=localhost/O=DevOps/C=US"

sudo chmod 600 /etc/nginx/ssl/selfsigned.key

echo "Certificate created successfully"