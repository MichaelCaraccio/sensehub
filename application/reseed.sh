#!/bin/bash

echo Deleting DB
docker exec -ti sensehub_app python3 /app/db_delete.py
echo Creating DB
docker exec -ti sensehub_app python3 /app/db_create.py
echo Seeding DB
docker exec -ti sensehub_app python3 /app/db_seed.py
