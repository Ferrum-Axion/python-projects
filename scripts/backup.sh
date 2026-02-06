#!/usr/bin/env bash
set -e

backup_dir="/var/backups/devops-site"
sudo mkdir -p "$backup_dir"

timestamp="$(date +%Y%m%d%H%M%S)"
backup_file="$backup_dir/backup_$timestamp.tar.gz"

echo "Creating backup..."
sudo tar -czf "$backup_file" -C /var/www devops-site

for old in $(sudo ls -t "$backup_dir"/backup_*.tar.gz | tail -n +6); do
    sudo rm -f "$old"
done

echo "Backup complete"