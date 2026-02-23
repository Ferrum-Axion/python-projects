#!/usr/bin/env bash
###############################################
# Purpose: check packages installed, deploy site, validate nginx, reload service, provide version of deployment
# Developer: Yaron Segev, Yar.Segev@gmail.com
# Version: 0.0.1
# Date: 3.2.2026
set -o errexit
set -o nounset
set -o pipefail
. helper.sh
###############################################

function main() {
    start_time=$SECONDS

    if [[ "$#" -ne 1 ]];
    then 
        printf "Must enter only 1 Parameter (allowed options: ssl/nossl)\n"
        writetolog "$start_time" "failed"
        exit 1
    else
        printf "1. Start: Verifying corret parametered entered\n"
        if ! checkenterdpar "$@";
        then 
           printf "The option you entered is not one of these: SSL/NOSSL\n"
        else
           printf "1. Done: corret parameter, site deployment selected $1\n"
        fi
    fi

    printf "2. Start: Verifying permission\n"
    if ! checksudo; 
    then 
       printf "Please rerun this script with elevated permissions\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "2. Done: Permission ok\n"
    fi
    
    printf "3. Start: Check all packages deployed.\n"
    if ! checkpackages; 
    then 
       printf "Installtion of $pkg failed, please check and rerun\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "3. Done: All packages ready\n"
    fi

    printf "4. Start: Deploying site\n"
    if ! deploysite; 
    then 
       printf "4. Please fix issue written above\n"
       writetolog "$start_time" "failed"
       exit 1
    else
       printf "4. Done: Site deployed succesfuly\n"
    fi

    printf "5. Start: Get Site version\n"
    siteversion
    printf "5. Done: Get site version\n"

    writetolog "$start_time" "success"
}


function writetolog() {
    local start_time="$1"
    local passfail="$2"
    duration=$(( SECONDS - start_time ))
    source ../.venv/bin/activate
    python3 ../log_tracker.py deploy $passfail $duration   
}


function checkenterdpar() {
    
    case $1 in
        ssl )
            DEPLOYCONF=$DEPLOYCONFSSL
            ;;
        nossl )
            DEPLOYCONF=$DEPLOYCONFNOSSL
            ;;
        * )
            return 1
            ;;
    esac
}

function siteversion() {
    siteversion=$(curl -sk https://devops-site.com)
    printf "   Site Version is: $siteversion\n"
}

function deploysite() {

    # copy index.html and health.html to var/www/devops-site
    for file in "$PROJECT_ROOT/site/"*; do
       cp -f "$file" "$SITEFOLDERWWW/site"
    done

    # delete default if exist in sites-enabled
    if [[ -e $NGINX_PATH/sites-enabled/default ]];
    then 
       rm -rf $NGINX_PATH/sites-enabled/default
       printf "Default site removed\n"
    fi
    
    # delete the other site not selected (e.g if ssl selected remove the not ssl in sites-enabled)
    if [ $DEPLOYCONF == "site.conf" ];   
    then 
        if [[ -e $NGINX_PATH/sites-enabled/site-ssl.conf ]];
        then 
           rm $NGINX_PATH/sites-enabled/site-ssl.conf
        fi
    else
        if [[ -e $NGINX_PATH/sites-enabled/site.conf ]];
        then 
           rm $NGINX_PATH/sites-enabled/site.conf
        fi
    fi

    # copy conf to site available and create soft link to site configuration
    cp -f $SITE_CONFIG/$DEPLOYCONF $NGINX_PATH/sites-available/

    if [  -e $NGINX_PATH/sites-enabled/$DEPLOYCONF ];
    then 
       rm $NGINX_PATH/sites-enabled/$DEPLOYCONF
    fi
    if ! ln -s $NGINX_PATH/sites-available/$DEPLOYCONF $NGINX_PATH/sites-enabled;
    then
       printf "Failed to create soft link, please check this\n"
       return 1
    fi

    # check configuration of nginx
    if ! nginx -t > $NULL 2>&1;
    then 
       printf "Site Health failed, please check configuration\n"
       return 1
    else 
       # restart nginx service
       if ! systemctl reload nginx;
       then 
          printf "Nginx Failed to reload,please check"
          return 1
       fi
    fi   
 
}


function checkpackages() {
    for pkg in ${PKG_LIST[@]}
        do
          if ! command -v $pkg > $NULL 2>&1;
          then
              printf "Missing: $pkg, wait for install\n"
              apt-get install -y $pkg
              if [ $? -ne 0 ];
              then 
                return 1
              fi
          fi
        done
}


###################
##   Main
###################
main "$@"