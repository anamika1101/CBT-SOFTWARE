# CBT Software — Computer Based Testing System

A full-stack web application for conducting computer-based examinations. Companies (exam organizers) create tests and question banks, assign them to exam centers, and students take the exam through a timed, AJAX-driven interface.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [System Architecture](#system-architecture)
4. [User Roles](#user-roles)
5. [Features](#features)
6. [Prerequisites](#prerequisites)
7. [Step-by-Step Setup](#step-by-step-setup)
8. [End-to-End User Flow](#end-to-end-user-flow)
9. [Environment Variables](#environment-variables)
10. [Project Structure](#project-structure)
11. [URL Reference](#url-reference)
12. [Database Models](#database-models)
13. [AI Question Generation](#ai-question-generation)
14. [Common Issues](#common-issues--fixes)
15. [Authors](#authors)

---

## Project Overview

CBT Software is a Django-based online examination platform designed to manage the complete lifecycle of a computer-based test — from question creation and center management to student exam delivery and result submission.

**Primary use-case:** A company (exam body) logs in, creates a test, adds questions (manually or via AI), registers exam centers, and students log in at those centers to take the timed MCQ exam.

---

## Tech Stack

| Layer        | Technology                                        |
|--------------|---------------------------------------------------|
| Backend      | Python 3.8+, Django 4.2                           |
| Database     | SQLite3 (default), compatible with MySQL          |
| Frontend     | HTML5, CSS3, JavaScript (ES6), Bootstrap 5        |
| REST API     | Django REST Framework 3.15                        |
| AI Features  | OpenAI API (optional)                             |
| Auth         | Custom session-based authentication               |
| Password     | Django `make_password` / `check_password` (PBKDF2)|

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    CBT Software                     │
├──────────────┬──────────────┬───────────────────────┤
│  general_zone│ companylogin │    centerlogin         │
│  (Public /   │ (Company     │  (Center Dashboard /  │
│   Auth)      │  Dashboard)  │   Entry Management)   │
├──────────────┴──────────────┴───────────────────────┤
│              studentexam (Exam Interface)            │
├─────────────────────────────────────────────────────┤
│              admin_zone (Super Admin)                │
├─────────────────────────────────────────────────────┤
│              SQLite3 Database (db.sqlite3)           │
└─────────────────────────────────────────────────────┘
```

---

## User Roles

| Role        | Access                                                                     |
|-------------|----------------------------------------------------------------------------|
| **Admin**   | Django admin panel + admin_zone — manages companies and centers            |
| **Company** | Creates/deletes tests, manages question bank (manual + AI), manages centers|
| **Center**  | Manages student entry, seat arrangement, emergency alerts                  |
| **Student** | Logs in at exam center, reads instructions, takes timed MCQ exam           |

---

## Features

### Company Portal
- Register and log in as a company
- Create and delete tests (Ongoing / Completed)
- Add and delete exam centers with hashed passwords
- Add questions manually with MCQ options and correct answer
- Filter questions by topic and difficulty
- **AI-powered question generation** using OpenAI API
- View ongoing and completed tests

### Center Portal
- Secure login with hashed password
- Student entry login management
- Seat arrangement view
- Emergency management page

### Student Exam Interface
- Timed MCQ exam (countdown timer)
- AJAX-based question navigation (Next / Previous)
- Mark for Review functionality
- Question palette showing attempt status
- Save & Next, Clear Response
- Auto-submit on timer expiry

### General / Public
- Public homepage, About, Services, Courses pages
- Company signup and login
- Center login
- Admin login
- Contact / Request Demo form
- Center listing page

---

## Prerequisites

Make sure the following are installed:

- **Python 3.8 or higher** — [Download](https://www.python.org/downloads/)
- **pip** (included with Python)
- **Git** — [Download](https://git-scm.com/)

Verify:

```bash
python --version
# or on macOS/Linux
python3 --version
```

---

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CBT-SOFTWARE.git
cd CBT-SOFTWARE
```

### 2. Create and Activate a Virtual Environment

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

You will see `(.venv)` prepended to your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

If you encounter errors for individual apps, run them explicitly:

```bash
python manage.py makemigrations companylogin
python manage.py makemigrations general_zone
python manage.py makemigrations admin_zone
python manage.py migrate
```

### 5. Create a Django Superuser

```bash
python manage.py createsuperuser
```

Use these credentials to log in at `/admin/`.

### 6. (Optional) Set OpenAI API Key

**macOS / Linux:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Windows:**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## End-to-End User Flow

### As a Company (Exam Organizer)

1. Go to **http://127.0.0.1:8000/** → Click **Company Sign Up** → fill in details
2. Log in with your email and password → lands on **Company Dashboard**
3. Sidebar → **Tests** → **Add Test** → enter test name, no. of questions, total marks
4. Sidebar → **Questions** → **Add Question** to add MCQs manually
   - OR click **Auto Generate** to generate via AI (requires `OPENAI_API_KEY`)
5. Sidebar → **Centers** → **+ Add Center** → fill in center details and set password
6. The test is now live — centers can log in and allow students to take the exam

### As a Center

1. Homepage → **Center Login** → enter center email and password
2. Access **Center Dashboard** → **Entry Login** to allow students
3. View **Student List** and manage **Seat Arrangement**

### As a Student

1. At the exam terminal → **http://127.0.0.1:8000/studhome/**
2. Enter credentials → click **Login**
3. Read **Instructions** → tick checkbox → click **Proceed**
4. Exam begins with countdown timer — navigate with Next/Previous, mark for review
5. Click **Submit** when done → confirmation page shown

### As Super Admin

1. **http://127.0.0.1:8000/admin/** → log in with superuser credentials
2. Manage all models (Companies, Centers, Questions, Tests) via Django admin

---

## Environment Variables

| Variable         | Required | Description                                         |
|------------------|----------|-----------------------------------------------------|
| `OPENAI_API_KEY` | Optional | Enables AI question generation on the Questions page|

Can also be set directly in [CBT/settings.py](CBT/settings.py) for development:

```python
OPENAI_API_KEY = "sk-your-key-here"
```

> Never commit real API keys to version control.

---

## Project Structure

```
CBT-SOFTWARE/
│
├── CBT/                        # Django project config
│   ├── settings.py             # Settings (DB, installed apps, static files)
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── general_zone/               # Public pages + Authentication
│   ├── models.py               # Company, Admin, contact_data, addnewCenterlist
│   ├── views.py                # Homepage, signup/login, center login
│   ├── urls.py
│   └── templates/
│
├── companylogin/               # Company portal
│   ├── models.py               # Test, Center, Question
│   ├── views.py                # Dashboard, tests, centers, questions, AI gen
│   ├── urls.py
│   └── templates/
│
├── centerlogin/                # Exam center portal
│   ├── views.py                # Dashboard, entry login, seat arrangement
│   ├── urls.py
│   └── templates/
│
├── studentexam/                # Student exam interface
│   ├── views.py                # Home, instructions, running exam, submit
│   ├── urls.py
│   └── templates/
│
├── admin_zone/                 # Super admin panel
│   ├── models.py               # Admin, Company, addnewCenterlist, contact_data
│   ├── views.py
│   └── urls.py
│
├── static/                     # Global static assets (CSS, JS, images)
├── media/                      # Uploaded files (e.g. center profile pics)
├── db.sqlite3                  # SQLite database (auto-created on migrate)
├── manage.py
├── requirements.txt
└── README.md
```

---

## URL Reference

| URL                          | Page / Purpose                     | Role     |
|------------------------------|------------------------------------|----------|
| `/`                          | Homepage                           | Public   |
| `/about/`                    | About page                         | Public   |
| `/services/`                 | Services page                      | Public   |
| `/comsignup/`                | Company signup (POST)              | Public   |
| `/comlogin/`                 | Company login (POST)               | Public   |
| `/centerlogin/`              | Center login (POST)                | Public   |
| `/adminlogin/`               | Admin login                        | Public   |
| `/admin/`                    | Django admin panel                 | Superuser|
| `/com_dashboard/`            | Company dashboard                  | Company  |
| `/addexam/`                  | Add new test form                  | Company  |
| `/ongoingtests/`             | Active tests list                  | Company  |
| `/completedtests/`           | Completed tests list               | Company  |
| `/tests/delete/<id>/`        | Delete a test                      | Company  |
| `/centers/`                  | Exam centers list                  | Company  |
| `/addcenter/`                | Add center (POST)                  | Company  |
| `/centers/delete/<id>/`      | Delete a center                    | Company  |
| `/questions/`                | Question bank                      | Company  |
| `/addquestion/`              | Add question (POST)                | Company  |
| `/questions/delete/<id>/`    | Delete a question                  | Company  |
| `/generate-questions/`       | AI question generation (POST)      | Company  |
| `/logout/`                   | Company logout                     | Company  |
| `/entrylogin/`               | Center entry login page            | Center   |
| `/cendashboard/`             | Center dashboard                   | Center   |
| `/studhome/`                 | Student exam home/login            | Student  |
| `/instruction/`              | Exam instructions page             | Student  |
| `/running/`                  | Running exam (AJAX MCQ)            | Student  |
| `/over/`                     | Exam submitted confirmation        | Student  |

---

## Database Models

### `Test` (companylogin)
| Field           | Type | Notes                        |
|-----------------|------|------------------------------|
| test_name       | Char | Name of the exam             |
| no_of_questions | Int  | Total question count         |
| total_marks     | Int  | Maximum marks                |
| status          | Char | `"Active"` or `"Completed"`  |

### `Center` (companylogin)
| Field       | Type | Notes                                    |
|-------------|------|------------------------------------------|
| center_name | Char | Name of exam center                      |
| address     | Char | Full address                             |
| phone       | Char | Contact number                           |
| email       | Char | Login email                              |
| profile_pic | File | Optional logo (upload_to='profile_pic/') |
| password    | Char | PBKDF2-SHA256 hashed password            |

### `Question` (companylogin)
| Field          | Type     | Notes                               |
|----------------|----------|-------------------------------------|
| question       | Char     | Question text (max 512 chars)       |
| option_1..4    | Char     | MCQ options                         |
| correct_option | Char     | Correct answer text                 |
| marks          | Int      | Marks for correct answer            |
| topic          | Char     | Subject topic (optional)            |
| difficulty     | Char     | Easy / Medium / Hard (optional)     |
| question_type  | Char     | Default: `"MCQ"`                    |
| generated_by   | Char     | `"manual"` or `"ai"`               |
| created_at     | DateTime | Auto-set on creation                |

### `Company` (admin_zone)
| Field    | Type  | Notes                         |
|----------|-------|-------------------------------|
| name     | Char  | Company / organization name   |
| email    | Email | Login email                   |
| phone    | Char  | Contact number                |
| password | Char  | PBKDF2-SHA256 hashed          |

---

## AI Question Generation

When `OPENAI_API_KEY` is configured:

1. Go to **Questions** page in the company portal
2. Click **Auto Generate**
3. Enter a **topic** (e.g. "Python Programming"), number of questions, and optional difficulty
4. The system calls OpenAI API, parses the response, and saves questions tagged `generated_by='ai'`
5. Questions appear immediately in the bank and can be filtered/deleted like any other

> Without an API key the manual question entry workflow functions normally.

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'django'` | Activate the virtual environment first |
| `migrate` fails | Run `makemigrations` for each app first |
| Static files (CSS/JS) not loading | Run `python manage.py collectstatic` |
| `OPENAI_API_KEY` not working | Re-export the variable in the current terminal session |
| Port 8000 already in use | Use `python manage.py runserver 8080` |

---

## Authors

| Name           | Role           | Contact                        |
|----------------|----------------|--------------------------------|
| Himanshu Singh | Lead Developer | himanshusingh945443@gmail.com  |
| Akash Anand    | Co-Developer   | 9765akashanand@gmail.com       |

---

## License

Built as a final year Computer Engineering Bachelor's project.
All rights reserved © CBT Software.
