#!/usr/bin/env bash
###############################################
# Purpose: take previous version of deployment and restore it
# Developer: Yaron Segev, Yar.Segev@gmail.com
# Version: 0.0.1
# Date: 2.2.2026
set -o errexit
set -o nounset
set -o pipefail
. helper.sh
BACKUPDIR=$PROJECT_ROOT/backups
##############################################


function main {
    printf "1. Start: Verifying permission\n"
    if ! checksudo; 
    then 
       printf "1. Please rerun this script with elevated permissions\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "1. Done: Permission ok\n"
    fi

    printf "2. Check Backup folder exist and at least 1 backup file exist\n"
    if ! checkbackupfolder; 
    then 
       printf "2. Backup folder/Valid backups do not exist cannot roll back\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "2. Folder and files exist moving on\n"
    fi

    printf "3. Perform Roll Back for site\n"
    if ! dorollback; 
    then 
       printf "3. Untar and restore failed, please check\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "3. Roll Back done\n"
    fi

    writetolog "$start_time" "success"
}


function writetolog() {
    local start_time="$1"
    local passfail="$2"
    duration=$(( SECONDS - start_time ))
    source ../.venv/bin/activate
    python3 ../log_tracker.py roll-back $passfail $duration   
}


function checkbackupfolder() {
    # check backup folder exist, and at least 1 file in it to do roll back
    if [ ! -d "$PROJECT_ROOT/backups" ];
    then 
       return 1
    else
       # Folder exist need to find at least 1 tar.gz backup file
       if  ! ls "$BACKUPDIR"/*.tar.gz 1>$NULL 2>&1 ;
       then
          return 1
       fi         
    fi  
}


function dorollback() {
    # find the newest file in backups and return its name
    latestfile=default
    checklatest=$( ls -1st "$BACKUPDIR"/*.tar.gz 2>$NULL | head -n 1 )
    latestfile="$(basename "$checklatest")"
    # untar the files to vr/www/devops-site folder with overwrite
    printf "   Restoring to $latestfile\n"
    if ! tar -xzf "$PROJECT_ROOT/backups/$latestfile" -C $SITEFOLDERWWW --overwrite;
    then
       return 1
    fi

}




###########################
#   Main
##########################
main