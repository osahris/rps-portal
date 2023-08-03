#!/bin/sh

exec docker-compose exec -T -u www-data nextcloud php occ $@
