@echo off
echo Setting up Django project...
python -m venv venv
call venv\Scriptsctivate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
pause
