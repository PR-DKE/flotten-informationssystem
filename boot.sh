#!/bin/bash
source venv/bin/activate
flask db upgrade
flask translate compile
cd src/
exec gunicorn -b :5000 --access-logfile - --error-logfile - main:app