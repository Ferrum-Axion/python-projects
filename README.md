# DevOps Web Task

This is my project for deploying a static website using NGINX with SSL and automation scripts.

## About the project

This project is about: setting up a web server, automating deployments, and managing backups. The site runs on NGINX with HTTPS (using a self-signed certificate), and I created some shell scripts to handle common tasks automatically.

## What's included

**Website files** - Just simple HTML pages in the `site/` folder. 

**NGINX configuration** - Two config files: one for HTTP that redirects everything to HTTPS, and one for HTTPS with the SSL certificate. The site runs on port 443 securely.

**Automation scripts** - I made 4 scripts to make life easier:
- `deploy.sh` - Pushes the site live and shows which version got deployed
- `backup.sh` - Creates timestamped backups and keeps only the last 5
- `health_check.sh` - Checks if the site is actually working
- `roll-back.sh` - Reverts to the previous backup if something breaks

## How it works

The deployment process copies files to `/var/www/devops-site`, validates the NGINX config, and reloads the server. Everything runs under a dedicated `webdeploy` user for security.

For SSL, I generate a self-signed certificate (browsers will warn about it, but that's fine for development). HTTP requests automatically redirect to HTTPS.

Backups are stored as compressed archives with timestamps. When rolling back, it extracts the second most recent backup (since the latest one is usually the broken deployment).

## Quick example

To deploy:
```bash
./scripts/deploy.sh
```

To rollback if something went wrong:
```bash
./scripts/roll-back.sh
```

That's pretty much it. 