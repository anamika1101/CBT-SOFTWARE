# CBT Authentication System - Complete Implementation Guide

## Overview
This documents the complete role-based authentication system for the CBT (Computer Based Test) platform with Company, Center, and Admin roles.

---

## 1. Database Models

### AppUser Model (Unified)
**Location:** `accounts/models.py`

```python
class AppUser(models.Model):
    """Unified user model - one account, role-based access."""
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    company_id = models.PositiveIntegerField(null=True, blank=True)
    center_id = models.PositiveIntegerField(null=True, blank=True)
    admin_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Role Choices
```python
class Role(models.TextChoices):
    COMPANY = 'COMPANY', 'Company'
    CENTER = 'CENTER', 'Center'
    ADMIN = 'ADMIN', 'Admin'
    STUDENT = 'STUDENT', 'Student'
```

### Legacy Models (Still Supported)
- **Company** - `admin_zone/models.py`
- **Center** - `companylogin/models.py`
- **Admin** - `admin_zone/models.py`

---

## 2. Authentication Views

### Company Authentication

**Login View:** `company_login_page`
- **URL:** `/login/company/`
- **Template:** `auth_company_login_form.html`
- **Features:**
  - Email and password authentication
  - Checks unified AppUser first (with hashed passwords)
  - Falls back to legacy Company model
  - Sets `com_id` in session on success
  - Redirects to `com_dashboard` after login

**Signup View:** `company_signup_page`
- **URL:** `/signup/company/`
- **Template:** `auth_company_signup_form.html`
- **Features:**
  - Creates new Company record
  - Creates AppUser with hashed password
  - Email validation (must be unique)
  - Password confirmation
  - Minimum 6 character password

### Center Authentication

**Login View:** `center_login_page`
- **URL:** `/login/center/`
- **Template:** `auth_center_login_form.html`
- **Features:**
  - Email and password authentication
  - Sets `center_id` in session on success
  - Redirects to `entrylogin` (center dashboard) after login

**Signup View:** `center_signup_page`
- **URL:** `/signup/center/`
- **Template:** `auth_center_signup_form.html`
- **Features:**
  - Creates new Center record
  - Creates AppUser with hashed password
  - Email validation (must be unique)
  - Password confirmation

### Admin Authentication

**Login View:** `admin_login_page`
- **URL:** `/login/admin/`
- **Template:** `auth_admin_login_form.html`
- **Features:**
  - Email and password authentication
  - Sets `admin_id` in session on success
  - Redirects to `adminhome` (admin dashboard) after login
  - **No signup** - Admin accounts created by superusers only

---

## 3. URL Configuration

**Location:** `general_zone/urls.py`

```python
urlpatterns = [
    # Login pages with forms
    path('login/company/', views.company_login_page, name='company_login_page'),
    path('signup/company/', views.company_signup_page, name='company_signup_page'),
    path('login/center/', views.center_login_page, name='center_login_page'),
    path('signup/center/', views.center_signup_page, name='center_signup_page'),
    path('login/admin/', views.admin_login_page, name='admin_login_page'),
    
    # Dashboard previews (show role capabilities)
    path('dashboard/company/', views.company_dashboard_preview, name='company_dashboard_preview'),
    path('dashboard/center/', views.center_dashboard_preview, name='center_dashboard_preview'),
    path('dashboard/admin/', views.admin_dashboard_preview, name='admin_dashboard_preview'),
]
```

---

## 4. Template Structure

### Login Form Templates
All login forms follow the same structure:

```html
<!-- Back button to navigate away -->
<a href="{% url 'homepage' %}" class="back-button">
    <i class="fas fa-arrow-left"></i>Back
</a>

<!-- Auth card with icon -->
<div class="auth-card">
    <div class="auth-header">
        <div class="auth-header-icon">
            <i class="fas fa-building"></i>
        </div>
        <h2>Role Name Login</h2>
    </div>
    
    <!-- Login form -->
    <form method="post" action="">
        {% csrf_token %}
        <input type="email" name="email" required>
        <input type="password" name="password" required>
        <button type="submit">Sign In</button>
    </form>
    
    <!-- Link to signup -->
    <a href="{% url 'role_signup_page' %}">Create an account</a>
</div>
```

### Signup Form Templates
Similar structure with additional fields:
- Name/Organization/Center Name
- Email
- Phone
- Password
- Confirm Password

---

## 5. Role-Based Access Control

### Decorator Usage
**Location:** `accounts/decorators.py`

```python
from accounts.decorators import require_role

@require_role('company')
def com_dashboard(request):
    # Only accessible with com_id in session
    pass

@require_role('center')
def center_dashboard(request):
    # Only accessible with center_id in session
    pass

@require_role('admin')
def admin_dashboard(request):
    # Only accessible with admin_id in session
    pass
```

### How It Works
1. Decorator checks if required role's ID is in session
2. If missing, redirects to homepage with warning message
3. If present, allows view execution

---

## 6. Authentication Flow

### Company Login Flow
```
Homepage
   ↓
[Click Login] → Modal appears
   ↓
[Company Login button]
   ↓
/login/company/ (company_login_page)
   ↓
Shows login form with:
- Email input
- Password input
- Back button (→ homepage)
- "Create Account" link (→ /signup/company/)
   ↓
[Submit Form]
   ↓
Checks AppUser first (hashed password)
Falls back to legacy Company model
   ↓
Sets request.session['com_id']
   ↓
Redirect to com_dashboard (Company Dashboard)
```

### Company Signup Flow
```
/signup/company/ (company_signup_page)
   ↓
Shows signup form with:
- Company Name
- Email
- Phone
- Password
- Confirm Password
- Back button (→ /login/company/)
   ↓
[Submit Form]
   ↓
Validate all fields
Check email uniqueness
Validate password match
Validate password length (min 6)
   ↓
Create Company record
Create AppUser with hashed password
Set role = 'COMPANY'
   ↓
Redirect to /login/company/ (with success message)
```

### Center & Admin Flows
Same as Company, but:
- Center redirects to `/entrylogin/` after login
- Admin redirects to `/adminhome/` after login
- Admin has no signup (superuser only)

---

## 7. Session Management

### Session Keys Used
```python
request.session['com_id']      # Company ID
request.session['center_id']   # Center ID
request.session['admin_id']    # Admin ID
```

### Session Checking
```python
# In views
if request.session.get('com_id'):
    # User is logged in as company
    
if request.session.get('center_id'):
    # User is logged in as center
    
if request.session.get('admin_id'):
    # User is logged in as admin
```

---

## 8. Back Button Implementation

### Back Button on Login Pages
```html
<a href="{% url 'homepage' %}" class="back-button">
    <i class="fas fa-arrow-left"></i>Back
</a>
```

### Back Button on Signup Pages
```html
<a href="{% url 'role_login_page' %}" class="back-button">
    <i class="fas fa-arrow-left"></i>Back to Login
</a>
```

**Styling:**
- Light background with border
- Hover effect with primary color
- Flexbox layout with icon + text
- Responsive and accessible

---

## 9. Error Handling

### Form Validation Errors
- Password mismatch → "Passwords do not match"
- Email already exists → "Email already registered"
- Missing fields → "All fields are required"
- Password too short → "Password must be at least 6 characters"

### Login Errors
- Invalid credentials → "Invalid email or password"
- Shows error messages using Django messages framework

### Display in Templates
```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

---

## 10. Security Features

### Password Hashing
- Uses Django's `make_password()` for new accounts
- Uses `check_password()` for authentication
- Legacy accounts gradually upgraded to hashed passwords

### CSRF Protection
- All forms include `{% csrf_token %}`
- Django middleware handles CSRF validation

### Session Security
- Session data validated using `require_role` decorator
- Prevents cross-role access

### Email Uniqueness
- Enforced at database model level
- Checked before account creation
- Prevents duplicate registrations

---

## 11. Testing Checklist

### Company Flow
- [ ] Can create account at `/signup/company/`
- [ ] Can login with created credentials at `/login/company/`
- [ ] Redirects to company dashboard after login
- [ ] Cannot access center/admin pages
- [ ] Back button works on all pages

### Center Flow
- [ ] Can create account at `/signup/center/`
- [ ] Can login with created credentials at `/login/center/`
- [ ] Redirects to center dashboard after login
- [ ] Cannot access company/admin pages
- [ ] Back button works on all pages

### Admin Flow
- [ ] Admin account pre-created by superuser
- [ ] Can login at `/login/admin/` with admin credentials
- [ ] Redirects to admin dashboard after login
- [ ] Cannot access company/center pages
- [ ] Back button works on page

### Cross-Role Prevention
- [ ] Company session cannot access center URLs
- [ ] Center session cannot access company URLs
- [ ] Non-logged users redirected to homepage

---

## 12. File Structure

```
general_zone/
├── templates/
│   ├── auth_company_login_form.html      ✨ NEW: Company login form
│   ├── auth_company_signup_form.html     ✨ NEW: Company signup form
│   ├── auth_center_login_form.html       ✨ NEW: Center login form
│   ├── auth_center_signup_form.html      ✨ NEW: Center signup form
│   ├── auth_admin_login_form.html        ✨ NEW: Admin login form
│   └── header.html                       (Updated: Points to login pages)
├── urls.py                               (Updated: Added signup routes)
└── views.py                              (Updated: New auth views)

accounts/
├── models.py                             (AppUser, Role)
└── decorators.py                         (@require_role)

admin_zone/
└── models.py                             (Admin, Company)

companylogin/
└── models.py                             (Center, Test, Question)
```

---

## 13. Troubleshooting

### "TemplateDoesNotExist" Error
- Ensure template files are in correct app's `templates/` folder
- Django searches: `app_name/templates/template.html`

### "NoReverseMatch" Error
- Check URL name in `urls.py` matches `{% url %}` in templates
- Ensure URL is included in main `CBT/urls.py`

### "Invalid email or password" on login
- Check password is hashed (use `set_password()`)
- Verify email exists in database
- Check `AppUser` model first, then legacy models

### Back button not working
- Ensure `{% url %}` tags resolve correctly
- Use absolute paths: `href="{% url 'homepage' %}"`
- Test back button in browser console

---

## 14. Future Enhancements

- [ ] Password reset via email
- [ ] Social media login (Google, GitHub)
- [ ] Remember me functionality
- [ ] Login attempt limits (prevent brute force)
- [ ] Activity logging
- [ ] Two-factor authentication
- [ ] Email verification for new accounts

---

## 15. Support & Questions

For issues or questions regarding this authentication implementation:
1. Check the troubleshooting section above
2. Review the file structure and installation
3. Verify all URL patterns are correctly registered
4. Check Django messages framework is configured
5. Ensure session middleware is enabled

---

**Last Updated:** February 20, 2026
**Version:** 1.0
**Status:** Production Ready
