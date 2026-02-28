from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from general_zone.serializers import CompanySerializer
from accounts.models import AppUser, Role

from .models import *
from companylogin.models import *
from admin_zone.models import *

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# from .models import Company
from .serializers import CompanySerializer

def homepage(request):
    return render(request,'homepage.html')

def about(request):
    return render(request,'about.html')

# Role-specific login landing pages (UI only; POST goes to existing auth views)

def company_login_page(request):
    """
    Company login form page.
    """
    if request.session.get('com_id'):
        return redirect('com_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 1. Check unified AppUser first
        try:
            app_user = AppUser.objects.get(email=email, role=Role.COMPANY)
            if app_user.check_password(password) and app_user.company_id:
                request.session['com_id'] = app_user.company_id
                messages.success(request, f'Welcome back, {app_user.name}!')
                return redirect('com_dashboard')
        except AppUser.DoesNotExist:
            pass
        
        # 2. Legacy: Company
        try:
            user = Company.objects.get(email=email)
            if user.password == password:
                request.session['com_id'] = user.id
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('com_dashboard')
        except Company.DoesNotExist:
            pass
        
        messages.error(request, 'Invalid email or password.')
    
    return render(request, 'auth_company_login_form.html')


def company_signup_page(request):
    """
    Company signup form page.
    """
    if request.session.get('com_id'):
        return redirect('com_dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not all([name, email, phone, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'auth_company_signup_form.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth_company_signup_form.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'auth_company_signup_form.html')
        
        if AppUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'auth_company_signup_form.html')
        
        if Company.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth_company_signup_form.html')
        
        # Create Company (legacy) + AppUser (unified)
        company = Company(name=name, phone=phone, email=email, password='')
        company.save()
        
        app_user = AppUser(email=email, name=name, phone=phone, role=Role.COMPANY, company_id=company.id)
        app_user.set_password(password)
        app_user.save()
        
        messages.success(request, 'Account created successfully! Please log in with your credentials.')
        return redirect('company_login_page')
    
    return render(request, 'auth_company_signup_form.html')


def center_login_page(request):
    """
    Center login form page.
    """
    if request.session.get('center_id'):
        return redirect('entrylogin')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 1. Check unified AppUser first
        try:
            app_user = AppUser.objects.get(email=email, role=Role.CENTER)
            if app_user.check_password(password) and app_user.center_id:
                request.session['center_id'] = app_user.center_id
                messages.success(request, f'Welcome back, {app_user.name}!')
                return redirect('entrylogin')
        except AppUser.DoesNotExist:
            pass
        
        # 2. Legacy: Center
        try:
            user = Center.objects.get(email=email)
            if user.password == password:
                request.session['center_id'] = user.id
                messages.success(request, f'Welcome back, {user.center_name}!')
                return redirect('entrylogin')
        except Center.DoesNotExist:
            pass
        
        messages.error(request, 'Invalid email or password.')
    
    return render(request, 'auth_center_login_form.html')


def center_signup_page(request):
    """
    Center signup form page.
    """
    if request.session.get('center_id'):
        return redirect('entrylogin')
    
    if request.method == 'POST':
        center_name = request.POST.get('name')  # Form sends 'name', we store as 'center_name'
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address', '')  # Optional address field
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not all([center_name, email, phone, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'auth_center_signup_form.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth_center_signup_form.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'auth_center_signup_form.html')
        
        if AppUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'auth_center_signup_form.html')
        
        if Center.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth_center_signup_form.html')
        
        # Create Center with center_name field
        center = Center(center_name=center_name, address=address, phone=phone, email=email, password='')
        center.save()
        
        app_user = AppUser(email=email, name=center_name, phone=phone, role=Role.CENTER, center_id=center.id)
        app_user.set_password(password)
        app_user.save()
        
        messages.success(request, 'Account created successfully! Please log in with your credentials.')
        return redirect('center_login_page')
    
    return render(request, 'auth_center_signup_form.html')


def admin_login_page(request):
    """
    Admin login form page - superuser only.
    """
    if request.session.get('admin_id'):
        return redirect('adminhome')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 1. Check unified AppUser first
        try:
            app_user = AppUser.objects.get(email=email, role=Role.ADMIN)
            if app_user.check_password(password) and app_user.admin_id:
                request.session['admin_id'] = app_user.admin_id
                messages.success(request, f'Welcome back, {app_user.name}!')
                return redirect('adminhome')
        except AppUser.DoesNotExist:
            pass
        
        # 2. Legacy: Admin
        try:
            user = Admin.objects.get(email=email)
            if user.password == password:
                request.session['admin_id'] = user.id
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('adminhome')
        except Admin.DoesNotExist:
            pass
        
        messages.error(request, 'Invalid email or password.')
    
    return render(request, 'auth_admin_login_form.html')


def student_login_page(request):
    """
    Student login / registration entry screen – actual exam flow handled in studentexam app.
    """
    return render(request, 'auth_student_login.html')

# Django restframework viewsets 

class CompanyViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        return Response({'success': False, 'errors': serializer.errors})
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            company = Company.objects.get(email=email, password=password)
            return Response({'success': True, 'company': CompanySerializer(company).data})
        except Company.DoesNotExist:
            return Response({'success': False, 'error': 'Invalid email or password'})


def comsignup(request):
    if request.method == 'POST':
        name = request.POST.get('com_signup_name') or request.POST.get('name')
        phone = request.POST.get('com_signup_phone') or request.POST.get('phone') or ''
        email = request.POST.get('com_signup_email') or request.POST.get('email')
        password = request.POST.get('com_signup_password') or request.POST.get('password')
        if AppUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered'})
        if Company.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already exists'})
        # Create Company (legacy) + AppUser (unified, hashed password)
        company = Company(name=name, phone=phone, email=email, password='')
        company.save()
        app_user = AppUser(email=email, name=name, phone=phone or '', role=Role.COMPANY, company_id=company.id)
        app_user.set_password(password)
        app_user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})  

def comLogin(request):
    try:
        if request.session.get('com_id'):
            return redirect('com_dashboard')
        if request.session.get('center_id'):
            return redirect('entrylogin')
        if request.session.get('admin_id'):
            return redirect('adminhome')
    except KeyError:
        pass
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # 1. Check unified AppUser first
        try:
            app_user = AppUser.objects.get(email=email)
            if app_user.check_password(password):
                if app_user.role == Role.COMPANY and app_user.company_id:
                    request.session['com_id'] = app_user.company_id
                    return redirect('com_dashboard')
                if app_user.role == Role.CENTER and app_user.center_id:
                    request.session['center_id'] = app_user.center_id
                    return redirect('entrylogin')
                if app_user.role == Role.ADMIN and app_user.admin_id:
                    request.session['admin_id'] = app_user.admin_id
                    return redirect('adminhome')
        except AppUser.DoesNotExist:
            pass
        # 2. Legacy: Company
        try:
            user = Company.objects.get(email=email)
            if user.password == password:
                request.session['com_id'] = user.id
                return redirect('com_dashboard')
        except Company.DoesNotExist:
            pass
        # 3. Legacy: Center
        try:
            user = Center.objects.get(email=email)
            if user.password == password:
                request.session['center_id'] = user.id
                return redirect('entrylogin')
        except Center.DoesNotExist:
            pass
        # 4. Legacy: Admin
        try:
            user = Admin.objects.get(email=email)
            if user.password == password:
                request.session['admin_id'] = user.id
                return redirect('adminhome')
        except Admin.DoesNotExist:
            pass
    return redirect('homepage')

def centerlogin(request):
    try:
        if request.session['center_id']:
            return redirect('entrylogin')
    except KeyError:
        pass
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Center.objects.get(email=email)
            if user.password == password:
                request.session['center_id'] = user.id
                return redirect('entrylogin')
        except Center.DoesNotExist:
            pass

    return redirect('homepage')

def admin_login(request):
    try:
        if request.session['admin_id']:
            return redirect('adminhome')
    except KeyError:
        pass
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Admin.objects.get(email=email)
            if user.password == password:
                request.session['admin_id'] = user.id
                return redirect('adminhome')
        except Admin.DoesNotExist:
            pass

    return redirect('homepage')

def courses(request):
    return render(request,'courses.html')

def services(request):
    return render(request,'services.html')

def request_demo(request):
    if request.method=='POST':
        name = request.POST.get('contact_name')
        email = request.POST.get('contact_email')
        phone = request.POST.get('contact_phone')
        organization = request.POST.get('contact_organization')
        message = request.POST.get('contact_message')
        
        contactdata = contact_data(
        name = name,
        email = email,
        phone = phone,
        organization=organization,
        message = message ) 
        contactdata.save()
        return JsonResponse({'success': True})     
    return JsonResponse({'success': False})

def centerlist(request):
    centers = addnewCenterlist.objects.all()
    return render(request, 'centerlist.html', {'centers': centers})

# Dashboard preview pages - show role capabilities without login
def company_dashboard_preview(request):
    """
    Company Dashboard preview - showcases what a company can do.
    """
    return render(request, 'com_dashboard_modern.html')


def center_dashboard_preview(request):
    """
    Center Dashboard preview - showcases what a center can do.
    """
    return render(request, 'cen_dashboard_modern.html')


def admin_dashboard_preview(request):
    """
    Admin Dashboard preview - showcases what an admin can do.
    """
    return render(request, 'admin_dashboard_modern.html')

# Logout views
def company_logout(request):
    """
    Logout company user and clear session.
    """
    if 'com_id' in request.session:
        del request.session['com_id']
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homepage')


def center_logout(request):
    """
    Logout center user and clear session.
    """
    if 'center_id' in request.session:
        del request.session['center_id']
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homepage')


def admin_logout(request):
    """
    Logout admin user and clear session.
    """
    if 'admin_id' in request.session:
        del request.session['admin_id']
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homepage')
