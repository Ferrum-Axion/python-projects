#!/usr/bin/env bash

URL="http://localhost"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")

if [ "$HTTP_CODE" -eq 200 ];
then
    echo "Healthy!"
    exit 0
else
    echo "Unhealthy: $HTTP_CODE"
    exit 1
fi
