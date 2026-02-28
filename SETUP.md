# CBT Software - Setup & Run Guide

## Quick Run (Windows)

### Option 1: Double-click `run.bat`
- Creates a virtual environment if needed
- Installs dependencies
- Runs migrations
- Starts the server at **http://127.0.0.1:8000**

### Option 2: PowerShell
```powershell
.\run.ps1
```

---

## Manual Setup

### 1. Install Python
- Install **Python 3.8+** from [python.org](https://www.python.org/downloads/)
- During installation, check **"Add Python to PATH"**

### 2. Open Terminal in project folder
```powershell
cd d:\CBT-SOFTWARE-master
```

### 3. Create virtual environment (optional but recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
> If you get "execution policy" error: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Install dependencies
```powershell
pip install -r requirements.txt
```

### 5. Run migrations
```powershell
python manage.py migrate
```

### 6. Start the server
```powershell
python manage.py runserver
```

### 7. Open in browser
**http://127.0.0.1:8000**

---

## Create Admin User (optional)
```powershell
python manage.py createsuperuser
```
Then visit: http://127.0.0.1:8000/admin/

---

## Troubleshooting

| Problem | Solution |
|--------|----------|
| **Python not found** | Install from [python.org](https://python.org) and check "Add to PATH". Use `py` instead of `python` on Windows if needed. |
| **pip not found** | Run `python -m pip install -r requirements.txt` |
| **Django not installed** | Run `pip install -r requirements.txt` (activate venv first) |
| **Access denied when installing** | 1) Use a virtual env: `python -m venv venv` then `.\venv\Scripts\Activate.ps1` 2) Or run terminal as Administrator 3) Or use `pip install --user -r requirements.txt` |
| **venv ensurepip fails** | Run Command Prompt as Admin and execute: `py -3 -m ensurepip --default-pip` |
| **Port 8000 in use** | Run `python manage.py runserver 8080` |
| **Migration errors** | Delete `db.sqlite3` and run `python manage.py migrate` again |
