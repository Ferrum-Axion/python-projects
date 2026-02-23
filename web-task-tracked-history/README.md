# devops-web-task

# Overview
This Project should be able to perform multiple things, 
such as deploy the site, create SSL certificate, backup or rollback, and perform site health check
as well after each shell log will be written to postgres operations database.

# Features:
1. Deploy script is used to deploy the site
2. Health check script use to check site health
3. ssl script used to create certificate is needed for the site
4. backup script will create backup of the site and save last 5 backups
5. roll back script will restore previous version of the site

# Installation

** all scripts must run as sudo in order to work correctly.
1. if you intend to use https please run ssl_selfsign.sh first to create a certificate
   by following information needed to enter when running it
2. if you want to deploy the site using:
   2.a. http only please run the following command ./deploy.sh nossl  (not case sensitive)
   2.b. https please run the following command ./deploy.sh ssl  (not case sensitive)
3. you can perform site health check at each time needed by running health_check.sh script.
4. you can create backup of the site by running backup.sh
5. you can roll back the site to previous version by running roll-back.sh 

# Configuration

1. The delpoy script will verify all dependencies and apps needed to deploy will be installed before.
2. please make sure the deployment needed (html files) will be under this project site folder.

# License Info
This project is licensed under the MIT License - see the LICENSE file for more details.


