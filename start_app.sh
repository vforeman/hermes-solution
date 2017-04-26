#!/bin/bash

python /app/manage.py db upgrade
python /app/hermes/app.py
