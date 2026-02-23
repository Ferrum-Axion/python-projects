#!/usr/bin/env bash
###############################################
# Purpose: return 0 if site healty
# Developer: Yaron Segev, Yar.Segev@gmail.com
# Version: 0.0.1
# Date: 2.2.2026
set -o errexit
set -o nounset
set -o pipefail
. helper.sh
###############################################


function main() {
    local start_time=$SECONDS

    printf "1. Verifying permission\n"
    if ! checksudo; 
    then 
       printf "1. Please rerun this script with elevated permissions\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "1. Done: Permission ok\n"
    fi

    printf "2. Checking Site configuration\n"
    if ! checkconfiguration; 
    then 
       printf "2. Site Health failed, please check configuration\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "2. Done: All ready, site configuration ok\n"
    fi

    printf "3. Checking Nginx active\n"
    if ! checknginxactive; 
    then 
       printf "3. Site not active, please check\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "3. Done: Nginx active\n"
    fi
    writetolog "$start_time" "success"
}


function writetolog() {
    local start_time="$1"
    local passfail="$2"
    duration=$(( SECONDS - start_time ))
    source ../.venv/bin/activate
    python3 ../log_tracker.py health_check $passfail $duration   
}


function checknginxactive() {
   if ! curl -I devops-site.com;
   then 
      exit 1
   fi
}


function checkconfiguration() {
    if ! nginx -t > $NULL 2>&1;
    then 
       exit 1
    fi
}


###################
##   Main
###################
main