#!/usr/bin/env bash
if curl -sf http://localhost/health.html > /dev/null; then
    echo "Site is healthy"
    exit 0
else
    echo "Site is down"
    exit 1
fi