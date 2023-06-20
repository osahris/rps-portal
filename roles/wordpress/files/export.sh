#!/bin/bash

# fail on errors
set -e

docker-compose run --rm -v $(pwd)/export/:/mnt/export/ db sh -c 'mysqldump --user=root --password=$MYSQL_ROOT_PASSWORD --host=db $MYSQL_DATABASE | gzip > /mnt/export/db.sql.gz'
docker-compose run --rm -u root -v $(pwd)/export/:/mnt/export/ wordpress-cli tar cz --exclude=debug.log  -f /mnt/export/wordpress.tar.gz .
