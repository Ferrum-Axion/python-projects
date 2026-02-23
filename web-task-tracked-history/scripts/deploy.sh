#!/usr/bin/env bash


PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

MY_SITE="$PROJECT_ROOT/site"
MY_CONFIG="$PROJECT_ROOT/nginx/site.conf"

SITE_DEST="/var/www/devops-site"
CONFIG_DEST="/etc/nginx/sites-available/devops-site"

echo "Starting Deploy..."

start_time=$SECONDS
start_ns=$(date +%s%N)

echo "PROJECT_ROOT=$PROJECT_ROOT"
echo "MY_SITE=$MY_SITE"
echo "MY_CONFIG=$MY_CONFIG"
echo "SITE_DEST=$SITE_DEST"
echo "CONFIG_DEST=$CONFIG_DEST"


sudo mkdir -p "$SITE_DEST"

sudo cp -r "$MY_SITE/"* "$SITE_DEST"

sudo cp "$MY_CONFIG" "$CONFIG_DEST"

sudo ln -sf "$CONFIG_DEST" "/etc/nginx/sites-enabled/devops-site"

sudo nginx -t

sudo systemctl reload nginx

echo "Deploy done!"
end_ns=$(date +%s%N)

duration=$(( SECONDS - start_time ))
duration_seconds=$(awk "BEGIN {printf \"%.3f\", ($end_ns - $start_ns)/1000000000}")
mydir="$(basename "$PWD")"
echo "$mydir"

source venv/bin/activate
python3 log_operations.py deploy success $duration_seconds

