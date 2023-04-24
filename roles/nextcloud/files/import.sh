#!/bin/bash

# fail on error
set -e

# shutdown wordpress
docker-compose down -v

# Import the Nextcloud database
cp ./import/nextclouddb.sql ./initdb/

# Import the Nextcloud folder
docker-compose run --rm -u root -v $(pwd)/import/nextcloud/:/mnt/import/nextcloud/:ro nextcloud /usr/bin/rsync -avrzP --sparse /mnt/import/nextcloud/ /var/www/html

# Import the Nextcloud data
docker-compose run --rm -u root -v $(pwd)/import/nextcloud-data/:/mnt/import/nextcloud-data/:ro nextcloud /usr/bin/rsync -avrzP --sparse /mnt/import/nextcloud-data/ /srv/nextcloud/data

