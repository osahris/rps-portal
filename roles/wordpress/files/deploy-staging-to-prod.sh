#!/bin/bash

set -e

TODAY=$(date -I)

mkdir -p wp-backup.{0,1,2,3}
# incremental backups
rm -rf wp-backup.3
mv wp-backup.2 wp-backup.3
mv wp-backup.1 wp-backup.2
cp -al wp-backup.0 wp-backup.1

mkdir -p wp-backup.0/html/

STAGING_CONTAINER_ID=$(docker-compose ps -q wordpress)
if [ -z "$STAGING_CONTAINER_ID" ]; then
    echo "Couldn't find staging container"
    exit 2
fi
STAGING_VOLUME=$(docker inspect $STAGING_CONTAINER_ID  | jq -r '.[0].Mounts[] | select(.Destination == "/var/www/html") | .Source')
if [ -z "$STAGING_VOLUME" ]; then
    echo "Couldn't find staging volume"
    exit 3
fi
STAGING_NETWORK=$(docker inspect $STAGING_CONTAINER_ID  | jq -r '.[0].NetworkSettings.Networks | to_entries | .[] | select(.key | contains("internal")) | .key')
if [ -z "$STAGING_NETWORK" ]; then
    echo "Couldn't find staging network"
    exit 3
fi

. env-prod

PROD_CONTAINER_ID=$(cd ../$PROD_SERVICE_NAME && docker-compose ps -q wordpress)
if [ -z "$PROD_CONTAINER_ID" ]; then
    echo "Couldn't find prod container"
    exit 2
fi
PROD_VOLUME=$(docker inspect $PROD_CONTAINER_ID  | jq -r '.[0].Mounts[] | select(.Destination == "/var/www/html") | .Source')
if [ -z "$PROD_VOLUME" ]; then
    echo "Couldn't find prod volume"
    exit 3
fi
PROD_NETWORK=$(docker inspect $PROD_CONTAINER_ID  | jq -r '.[0].NetworkSettings.Networks | to_entries | .[] | select(.key | contains("internal")) | .key')
if [ -z "$PROD_NETWORK" ]; then
    echo "Couldn't find prod network"
    exit 3
fi

# backup wp assets
rsync -az --delete $STAGING_VOLUME/ wp-backup.0/html/

. env-mysql

# dump staging db to backup folder
docker run --rm --network=$STAGING_NETWORK -v $(pwd)/wp-backup.0:/backupdata mysql:5.7 \
    mysqldump -h db \
          -u wordpress \
          --password=$MYSQL_PASSWORD \
          wordpress  \
          --result-file="/backupdata/$TODAY-dump.sql" \
          --add-drop-database=FALSE \
          --add-drop-table=FALSE \
          --all-databases=FALSE \
          --all-tablespaces \
          --comments \
          --complete-insert \
          --create-options=TRUE \
          --default-character-set=utf8mb4 \
          --dump-date \
          --lock-tables=TRUE \
          --log-error=error.log \
          --no-create-db=TRUE \
          --no-create-info=FALSE \
          --no-data=FALSE \
          --set-charset=TRUE \
          --skip-add-drop-table=TRUE \
          --skip-add-locks=FALSE \
          --skip-comments=FALSE \
          --skip-compact=FALSE \
          --skip-set-charset=FALSE;

# push assets to production
rsync -a --delete --exclude=wp-config.php --exclude=.htaccess wp-backup.0/html/ $PROD_VOLUME/

. ../$PROD_SERVICE_NAME/env-mysql

rm -f importer.sql
echo "DROP DATABASE wordpress;
CREATE DATABASE wordpress character set UTF8mb4 collate utf8mb4_bin;
USE wordpress;
SET NAMES 'utf8mb4';
SOURCE /backupdata/$TODAY-dump.sql;
EXIT" > importer.sql

# restore db backup to production
docker run -i --rm --network=$PROD_NETWORK -v $(pwd)/wp-backup.0:/backupdata mysql:5.7 \
    mysql -h db \
          -u wordpress \
          --password=$MYSQL_PASSWORD \
          wordpress < "importer.sql"

if [ "$?" == "0" ]; then
    echo "SUCCESS"
fi