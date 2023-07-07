#!/bin/sh

exec docker-compose exec -u www-data nextcloud php occ $@
