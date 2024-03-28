#!/bin/bash
so
CREATE_DB="CREATE DATABASE IF NOT EXISTS $PGDB;"
CREATE_ROLE="CREATE ROLE IF NOT EXISTS $PGUSER WITH LOGIN PASSWORD '$PGPASSWORD';"
GRANT_PREV="GRANT ALL PRIVILEGES ON DATABASE $PGDB TO $PGUSER;"


wait_for_postgres() {


    until psql -v ON_ERROR_STOP=1 -U postgres  -c '\l'; do
        echo "Waiting for PostgreSQL to become available..."
        sleep 1
    done
}

wait_for_postgres &

psql -U postgres -c "$CREATE_DB" &&
psql -U postgres -c "$CREATE_ROLE" &&
psql -U postgres -c "$GRANT_PREV" &&


if [ -f "$PATH_TO_SQL" ]; then
    # Restore the backup file
    $POSTRGES_PASSWORD psql -U postgres -d "$PGDB" -f $PATH_TO_SQL

    else
      echo "Error upload dump"
fi



# Continue with the default entrypoint command
exec "$@"

