# CHP Project - Django Web Application

## Quick Start

### Option 1: Run with One Click
- **Windows:** Double-click `run.bat`
- **Mac/Linux:** Double-click `run.sh` or run `./run.sh` in terminal

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scriptsctivate     # Windows

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Then open http://localhost:8000 in your browser.
