web: python manage.py migrate && gunicorn cbo_site.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
