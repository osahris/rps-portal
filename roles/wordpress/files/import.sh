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
