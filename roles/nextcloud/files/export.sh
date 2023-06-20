
# database
docker-compose exec -T -u postgres postgres pg_dump > export/nextclouddb.sql || rm export/nextclouddb.sql

# Export the Nextcloud folder
docker-compose run --rm -u root --no-deps -v $(pwd)/export/nextcloud/:/mnt/export/nextcloud/ nextcloud /usr/bin/rsync -avrzP --sparse /var/www/html/ /mnt/export/nextcloud/

# Export the Nextcloud data
docker-compose run --rm -u root --no-deps -v $(pwd)/export/nextcloud-data/:/mnt/export/nextcloud-data/ nextcloud /usr/bin/rsync -avrzP --sparse /srv/nextcloud/data/ /mnt/export/nextcloud-data/
