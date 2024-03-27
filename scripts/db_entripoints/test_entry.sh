#!/bin/bash
wait_for_postgres() {


    until psql -v ON_ERROR_STOP=1 -U postgres  -c '\l'; do
        echo "Waiting for PostgreSQL to become available..."
        sleep 1
    done

    echo "Pg is started"
}

wait_for_postgres