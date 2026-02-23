#!/usr/bin/env bash
###############################################
# Purpose: contains repeated functions
# Developer: Yaron Segev, Yar.Segev@gmail.com
# Version: 0.0.1
# Date: 8.2.2026
set -o errexit
set -o nounset
set -o pipefail
##############################################
PROJECT_ROOT="$(cd "$(dirname "$0")/../" && pwd)"
SITEFOLDERWWW=/var/www/devops-site
SAVESTRING=devops-site
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
FILEPATTERN="${SAVESTRING}-${TIMESTAMP}"
PKG_LIST=(nginx openssl)
NGINX_PATH=/etc/nginx
SITE_CONFIG=$PROJECT_ROOT/nginx
DEPLOYCONFNOSSL=site.conf
DEPLOYCONFSSL=site-ssl.conf
DEPLOYCONF=$DEPLOYCONFNOSSL
SSLLOCATION=/etc/nginx/ssl
NULL=/dev/null


function checksudo() {
    if [[ $EUID != 0 ]] ; 
    then
       return 1
    fi 
    return 0
}