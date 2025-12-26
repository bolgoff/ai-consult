#!/bin/bash

set -e

echo "Qdrant"
sleep 5

echo "Vectors to db"
python3 data_to_vdb.py

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
