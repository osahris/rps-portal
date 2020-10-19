#!/bin/bash

TODAY=$(date -I)

mkdir -p wp-backup.0/html/

# incremental backups
rm -rf wp-backup.3
mv wp-backup.2 wp-backup.3
mv wp-backup.1 wp-backup.2
cp -al wp-backup.0 wp-backup.1

# backup wp assets
rsync -az --delete /var/www/napkon-staging/ wp-backup.0/html/

# dump staging db to backup folder
mysqldump -u root \
          napkonstaging  \
          --result-file="wp-backup.0/$TODAY-dump.sql" \
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
rsync -a --delete --exclude=wp-config.php wp-backup.0/html/ /var/www/napkon-prod/

rm importer.sql
echo "DROP DATABASE napkonprod;
CREATE DATABASE napkonprod character set UTF8mb4 collate utf8mb4_bin;
USE napkonprod;
SET NAMES 'utf8mb4';
SOURCE wp-backup.0/$TODAY-dump.sql;
EXIT" > importer.sql

# restore db backup to production
mysql -u root < "importer.sql"
