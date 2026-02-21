#!/usr/bin/env bash


BACKUP_DIR="$HOME/backups"
DEST_DIR="/var/www/devops-site"

LATEST=$(ls -t "$BACKUP_DIR"/site_*.tar.gz | head -n 1)

if [ -z "$LATEST" ];
then
    echo "No backups found!"
    exit 1
fi

sudo rm -rf "${DEST_DIR:?}"/*

sudo tar -xzf "$LATEST" -C "$DEST_DIR"

sudo systemctl reload nginx



echo "Rollback done!"
