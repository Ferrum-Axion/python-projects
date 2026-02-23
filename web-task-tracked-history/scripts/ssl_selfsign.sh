#!/usr/bin/env bash
###############################################
# Purpose: generate self sign ssl cert safely
# Developer: Yaron Segev, Yar.Segev@gmail.com
# Version: 0.0.1
# Date: 2.2.2026
set -o errexit
set -o nounset
set -o pipefail
. helper.sh
###############################################

function main() {
   start_time=$SECONDS

   printf "1. Create SSL, please fill up what is needed\n"
   createssl
   printf "1. Done creating SSL Certificate\n" 

   writetolog "$start_time" "success"
}


function writetolog() {
    local start_time="$1"
    local passfail="$2"
    duration=$(( SECONDS - start_time ))
    source ../.venv/bin/activate
    python3 ../log_tracker.py roll-ssl_selfsign $passfail $duration   
}

function createssl() {
   sudo openssl req -x509 -nodes -newkey rsa:2048 \
     -keyout $SSLLOCATION/site.key \
     -out $SSLLOCATION/site.crt \
     -days 365
}


#################
# MAIN
################
main