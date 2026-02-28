# CBT-SOFTWARE

## How To Run (Windows)

1. Create and activate virtual environment:
   - `python -m venv venv`
   - `venv\Scripts\activate`
2. Install dependencies:
   - `python -m pip install -r requirements.txt`
3. Apply migrations:
   - `python manage.py migrate`
4. Start server:
   - `python manage.py runserver`
5. Open:
   - `http://127.0.0.1:8000`

You can also use one-click launch scripts:
- `run.bat`
- `run.ps1`

## Demo Credentials (bundled SQLite)
- Company: `hs@gmail.com` / `1234`
- Center: `kashi@gmail.com` / `1234`
- Admin: `kashi@gmail.com` / `1234`

## Features
- Role-based login and dashboards (Company, Center, Admin)
- Exam and question management
- Center and company management
- API endpoints via Django REST Framework

## Built Using
- Django
- SQLite
- HTML/CSS/JavaScript
- Bootstrap
