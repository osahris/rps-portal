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

# backup wp assets
rsync -az --delete $(docker volume inspect staging_wordpress -f "{{ .Mountpoint }}")/ wp-backup.0/html/

. env-mysql

# dump staging db to backup folder
docker run --rm --network=staging_wordpress-internal -v $(pwd)/wp-backup.0:/backupdata mysql:5.7 \
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
rsync -a --delete --exclude=wp-config.php --exclude=.htaccess wp-backup.0/html/ $(docker volume inspect prod_wordpress -f "{{ .Mountpoint }}")/

. ../prod/env-mysql

rm -f importer.sql
echo "DROP DATABASE wordpress;
CREATE DATABASE wordpress character set UTF8mb4 collate utf8mb4_bin;
USE wordpress;
SET NAMES 'utf8mb4';
SOURCE /backupdata/$TODAY-dump.sql;
EXIT" > importer.sql

# restore db backup to production
docker run -i --rm --network=prod_wordpress-internal -v $(pwd)/wp-backup.0:/backupdata mysql:5.7 \
    mysql -h db \
          -u wordpress \
          --password=$MYSQL_PASSWORD \
          wordpress < "importer.sql"

if [ "$?" == "0" ]; then
    echo "SUCCESS"
fi