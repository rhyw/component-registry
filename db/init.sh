#!/bin/bash

set -e

POSTGRES="psql --username ${POSTGRES_USER}"

# Create the database
$POSTGRES <<-EOSQL
CREATE DATABASE ${APP_DB_NAME};
EOSQL

# Create the user with read/write permission to the database
$POSTGRES <<-EOSQL
CREATE USER "${APP_DB_USER}" WITH PASSWORD '${APP_DB_PASS}';
GRANT ALL PRIVILEGES ON DATABASE ${APP_DB_NAME} TO "${APP_DB_USER}";
EOSQL
