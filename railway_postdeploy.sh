#!/bin/bash
# railway_postdeploy.sh

# Run migrations
python manage.py migrate

# Run the setup_demo_data command
python manage.py setup_demo_data

# Collect static files (just to be safe)
python manage.py collectstatic --noinput