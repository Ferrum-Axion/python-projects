#!/usr/bin/env bash
###############################################
# Purpose: create timestamp backup, keep last 5
# Developer: Yaron Segev, Yar.Segev@gmail.com
# Version: 0.0.1
# Date: 2.2.2026
set -o errexit
set -o nounset
set -o pipefail
. helper.sh
###############################################


function main {
    start_time=$SECONDS

    printf "1. Start: Verifying permission\n"
    if ! checksudo; 
    then 
       printf "Please rerun this script with elevated permissions\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "1. Done: Permission ok\n"
    fi

    printf "2. Perform Backup for site\n"
    if ! dobackup; 
    then 
       printf "2. Failed to perform backup\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "2. Backup done\n"
    fi

    printf "3. Deleting older backups if exist\n"
    if ! deleteoldbackup; 
    then 
       printf "Failed to delete the old backups, please check\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "3. Done\n"
    fi
    writetolog "$start_time" "success"
}


function writetolog() {
    local start_time="$1"
    local passfail="$2"
    duration=$(( SECONDS - start_time ))
    source ../.venv/bin/activate
    python3 ../log_tracker.py backup $passfail $duration   
}


function dobackup() {
    # check backup folder exist if not create it
    if [[ ! -d $PROJECT_ROOT/backups ]];
    then 
       mkdir -p $PROJECT_ROOT/backups
    fi    
    filename="$FILEPATTERN.tar.gz"
    printf "   File name: $filename\n"
    if ! tar -czf "$PROJECT_ROOT/backups/$filename" -C "$SITEFOLDERWWW" site;
    then 
       return 1
    fi
}

function deleteoldbackup() {
    backupdir=$PROJECT_ROOT/backups
    # make a list and sort newest first, find only .tar.gz files, show from 6+ (more than 5) and delete these
    if ! ls -1t "$backupdir"/*.tar.gz 2>$NULL | tail -n +6 | xargs rm -f;
    then 
       return 1
    fi
}


###########################
#   Main
##########################
main