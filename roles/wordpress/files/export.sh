#!/bin/bash

docker-compose run --rm -T db sh -c 'exec mysqldump --user=root --password=$MYSQL_ROOT_PASSWORD --host=db $MYSQL_DATABASE' | gzip > export/db.sql.gz
docker-compose run --rm -u root -T wordpress-cli tar cz . > export/wordpress.tar.gz
