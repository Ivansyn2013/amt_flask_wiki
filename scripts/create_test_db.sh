#!/bin/bash
set -e
set -x
#source .env

CREATE_DB="CREATE DATABASE $PGDB;"
CREATE_ROLE="CREATE ROLE $PGUSER WITH LOGIN PASSWORD '$PGPASSWORD';"
GRANT_PREV="GRANT ALL PRIVILEGES ON DATABASE $PGDB TO $PGUSER;"
CHANGE_TABLES_OWNER="SELECT 'ALTER TABLE public.' || tablename || ' OWNER TO $PGUSER;' FROM pg_tables WHERE schemaname = 'public';"
UNIX_HOST="/var/run/postgresql"

wait_for_postgres() {


    until psql -v ON_ERROR_STOP=1 -h $UNIX_HOST -U postgres -d postgres -c '\q'; do
        echo "Waiting for PostgreSQL to become available..."
        sleep 2
    done

}

wait_for_postgres

psql -h $UNIX_HOST -U postgres -c "$CREATE_DB" &&           echo "Create db $PGDB success"
psql -h $UNIX_HOST -U postgres -c "$CREATE_ROLE" &&         echo "Create role $PGUSER success"
psql -h $UNIX_HOST -U postgres -c "$GRANT_PREV" &&          echo "Create grant prev success"
psql -h $UNIX_HOST -U postgres -c "$CHANGE_TABLES_OWNER" && echo "Create table owner change success"
psql -h $UNIX_HOST -U postgres -d "$PGDB" -f /backup/2024-08-20-wiki-backup.sql \
 && echo "Upload backup success"

# Continue with the default entrypoint command
exec "$@"

