#!/usr/bin/env bash
#
# reset table hashes

set -e
set -u

# Set these environmental variables to override them,
# but they have safe defaults.
export PGHOST=${PGHOST-postgresvm}
export PGPORT=${PGPORT-5432}
export PGDATABASE=${PGDATABASE-remcom}
export PGUSER=${PGUSER-consol}
export PGPASSWORD=${PGPASSWORD-123}

RUN_PSQL="psql -X --set AUTOCOMMIT=off --set ON_ERROR_STOP=on "

${RUN_PSQL} <<SQL
drop table if exists hashes;

create table hashes(
        id serial,
        name text,
        date date default now(),
        hash text primary key
        );
commit;


SQL
