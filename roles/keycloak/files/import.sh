#!/bin/bash

# Fail on errors
set -e

# Read credentials from env file
source env-keycloak

# Import data from all .json files to the keycloak service
docker-compose exec -u keycloak -e PGPASSWORD=$KC_DB_PASSWORD keycloak /opt/keycloak/bin/kc.sh --verbose import --dir /opt/keycloak/data/import/
