#!/bin/sh

# fail on errors
set -e

# export the database
EXPORT_DB_DIR=$(mktemp -d)
docker-compose exec -T -u postgres postgres pg_dump > $EXPORT_DB_DIR/nextclouddb.sql || rm $EXPORT_DB_DIR/nextclouddb.sql
tar -cC $EXPORT_DB_DIR nextclouddb.sql
rm -r $EXPORT_DB_DIR

# Export the Nextcloud folder
docker-compose run --rm -u root --no-deps -v $(pwd)/export/nextcloud/:/mnt/export/nextcloud/ nextcloud /usr/bin/rsync -avrzP --sparse /var/www/html/ /mnt/export/nextcloud/

# Export the Nextcloud data
docker-compose run --rm -u root --no-deps -v $(pwd)/export/nextcloud-data/:/mnt/export/nextcloud-data/ nextcloud /usr/bin/rsync -avrzP --sparse /srv/nextcloud/data/ /mnt/export/nextcloud-data/
