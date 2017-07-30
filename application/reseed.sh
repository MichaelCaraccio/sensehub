#!/bin/bash

echo Deleting DB
python db_delete.py
echo Creating DB
python db_create.py
echo Seeding DB
python db_seed.py
