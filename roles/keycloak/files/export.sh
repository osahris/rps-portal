#!/bin/bash

# Fail on errors
set -e

# Read credentials from env file
source env-keycloak

# Export all .json data files to the keycloak service
# Note that the user is root to allow export of the master realm
docker-compose exec -u root -e PGPASSWORD=$KC_DB_PASSWORD keycloak /opt/keycloak/bin/kc.sh --verbose export --dir /opt/keycloak/data/export/
