#!/bin/bash
set +x
source .env

CREATE_DB="CREATE DATABASE  $PGDB;"
CREATE_ROLE="CREATE ROLE $PGUSER WITH LOGIN PASSWORD '$PGPASSWORD';"
CREATE_DB="CREATE DATABASE IF NOT EXISTS $PGDB;"
CREATE_ROLE="CREATE ROLE IF NOT EXISTS $PGUSER WITH LOGIN PASSWORD '$PGPASSWORD';"
GRANT_PREV="GRANT ALL PRIVILEGES ON DATABASE $PGDB TO $PGUSER;"
CHANGE_TABLES_OWNER="SELECT 'ALTER TABLE public.' || tablename || ' OWNER TO $PGUSER;' FROM pg_tables WHERE schemaname = 'public';"

wait_for_postgres() {


    until psql -v ON_ERROR_STOP=1 -U postgres  -c '\l'; do
        echo "Waiting for PostgreSQL to become available..."
        sleep 1
    done
}

wait_for_postgres 

psql -U postgres -c "$CREATE_DB" &&           echo "Create db $PGDB success"
psql -U postgres -c "$CREATE_ROLE" &&         echo "Create role $PGUSER success" 
psql -U postgres -c "$GRANT_PREV" &&          echo "Create grant prev success"     
psql -U postgres -c "$CHANGE_TABLES_OWNER" && echo "Create table owner change success" 

if [ -f "$PATH_TO_SQL" ]; then
    # Restore the backup file
    $POSTRGES_PASSWORD psql -U postgres -d "$PGDB" < $PATH_TO_SQL

    echo "Dump upladed"
	else
	      echo "Error upload dump"
fi



# Continue with the default entrypoint command
exec "$@"

