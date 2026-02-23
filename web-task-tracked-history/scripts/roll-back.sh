#!/usr/bin/env bash
###################
#
# Created by: Elena Kuznetsov
# Purpose: Rollback site to the latest backup
# Version: 0.0.2
# Date: 7/2/2026
#
###################

#!/usr/bin/env bash

START_TIME=$(date +%s)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$HOME/backups"
DEST_DIR="/var/www/devops-site"

echo "Starting the rolling back proccess... lets search for the latest backup..."

LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/fasloli_site_backup_*.tar.gz 2>/dev/null | head -n 1)

if [ -z "$LATEST_BACKUP" ];
then
    echo "Panic! No backups found in $BACKUP_DIR. We are doomed, good luck"
    exit 1
fi

echo "Found it, restoring from the: $LATEST_BACKUP"

sudo rm -rf "${DEST_DIR:?}"/*

if sudo tar -xzf "$LATEST_BACKUP" -C "$DEST_DIR";
then
    echo "Success! The site has been restored to its former glory, reloading nginx..."
    sudo systemctl reload nginx
    echo "Nginx reloaded, check the site now!"

    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    source "$PROJECT_ROOT/.venv/bin/activate"
    python3 "$PROJECT_ROOT/log_tracker.py" "rollback" "success" "$DURATION"

    exit 0
else
    echo "Oh crap, something went wrong, sorry"
    exit 1
fi