#!/bin/bash
echo "Setting up Django project..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
