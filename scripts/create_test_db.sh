#!/bin/bash
set +e
source .env

CREATE_DB="CREATE DATABASE $PGDB_TEST;"
CREATE_ROLE="CREATE ROLE $PGUSER WITH LOGIN PASSWORD '$PGPASSWORD';"
GRANT_PREV="GRANT ALL PRIVILEGES ON DATABASE $PGDB_TEST TO $PGUSER;"
CHANGE_TABLES_OWNER="SELECT 'ALTER TABLE public.' || tablename || ' OWNER TO $PGUSER;' FROM pg_tables WHERE schemaname = 'public';"

wait_for_postgres() {


    until psql -v ON_ERROR_STOP=1 -U postgres  -c '\l'; do
        echo "Waiting for PostgreSQL to become available..."
        sleep 1
    done
}

wait_for_postgres 

psql -U postgres -c "$CREATE_DB" &&           echo "Create db $PGDB_TEST success"
psql -U postgres -c "$CREATE_ROLE" &&         echo "Create role $PGUSER success" 
psql -U postgres -c "$GRANT_PREV" &&          echo "Create grant prev success"     
psql -U postgres -c "$CHANGE_TABLES_OWNER" && echo "Create table owner change success" 


# Continue with the default entrypoint command
exec "$@"

