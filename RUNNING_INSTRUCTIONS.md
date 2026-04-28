
0. Install latest version of python: [https://www.python.org/](https://www.python.org/)
1. Create and activate a virtual environment: `python -m venv .venv`
2. Activate virtual environment: `.\\.venv\\Scripts\\activate.bat` (windows), `source .venv/bin/activate` (Linux)
3. Install requirements: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Run server: `python manage.py runserver`
