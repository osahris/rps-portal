
# database
docker-compose run --rm -v $(pwd)/export/:/mnt/export/ postgres pg_dump -h postgres -U nextcloud -f /mnt/export/nextclouddb.sql nextcloud

# Export the Nextcloud folder
docker-compose run --rm -u root --no-deps -v $(pwd)/export/nextcloud/:/mnt/export/nextcloud/ nextcloud /usr/bin/rsync -avrzP --sparse /var/www/html/ /mnt/export/nextcloud/

# Export the Nextcloud data
docker-compose run --rm -u root --no-deps -v $(pwd)/export/nextcloud-data/:/mnt/export/nextcloud-data/ nextcloud /usr/bin/rsync -avrzP --sparse /srv/nextcloud/data/ /mnt/export/nextcloud-data/
