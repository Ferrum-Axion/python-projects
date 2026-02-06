#!/usr/bin/env bash
set -e
backup_dir="/var/backups/devops-site"

echo "Looking for previous backup..."
previous_backup=$(ls -t "$backup_dir"/backup_*.tar.gz | sed -n '2p')

if [ -z "$previous_backup" ]; then
  echo "Error: No previous backup found"
  exit 1
fi

echo "Rolling back to previous version..."

# Extract and reload
sudo tar -xzf "$previous_backup" -C /var/www/
sudo systemctl reload nginx

echo "Rollback completed"