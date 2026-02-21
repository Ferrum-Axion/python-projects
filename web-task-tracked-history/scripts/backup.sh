#!/usr/bin/env bash

BACKUP_DIR="$HOME/backups"
SITE_DIR="/var/www/devops-site"

mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

sudo tar -czf "$BACKUP_DIR/site_$TIMESTAMP.tar.gz" -C "$SITE_DIR" .

echo "Backup created!"

ls -t "$BACKUP_DIR"/site_*.tar.gz | tail -n +6 | xargs rm -f
