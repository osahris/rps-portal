#!/bin/bash

# fail on errors
set -e

# shutdown wordpress
docker-compose down -v

# copy database dump
cp ./import/db.sql* ./initdb/

# copy wordpress files
docker-compose run --rm -u root -v $(pwd)/import/:/mnt/import/:ro wordpress-cli tar xzf /mnt/import/wordpress.tar.gz

# bring the docker-compose stack up again
docker-compose up -d

echo "wordpress user and meta data will be deleted"
docker-compose run --rm -v $(pwd)/export/:/mnt/export/ db sh -c "mysql -u <user> -p -e 'DELETE FROM wp_usermeta WHERE user_id NOT IN (1)'"
docker-compose run --rm -v $(pwd)/export/:/mnt/export/ db sh -c "mysql -u <user> -p -e 'DELETE FROM wp_users WHERE user_id NOT IN (1)'"

# wp user delete $(wp user list --field=ID) --reassign=2
# wp db query	"DELETE FROM wp_usermeta WHERE user_id NOT IN (1);"
# wp db query	"DELETE FROM wp_users WHERE ID NOT IN (1);"