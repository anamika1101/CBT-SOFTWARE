from django.shortcuts import render,redirect
from django.core.exceptions import *
from accounts.decorators import require_role
from .models import  *
from general_zone.models import *
from centerlogin.models import *
from companylogin.models import *

@require_role('admin')
def admin_home(request):
    user_id = request.session.get('admin_id')
    Admin_data = Admin.objects.get(id=user_id)
    all_contacts = contact_data.objects.all()
    Companys = Company.objects.all()
    Centers = Center.objects.all()
    Tests = Test.objects.all()

    return render(request, 'admin_dashboard_modern.html', {
        'contacts': all_contacts,
        'Companys': Companys,
        'Centers': Centers,
        'Tests': Tests,
        'Admin_data': Admin_data,
    })

@require_role('admin')
def admin_logout(request):
    if request.session.get('admin_id'):
        del request.session['admin_id']
    return redirect('homepage')

@require_role('admin')
def add_center(request):
    if request.method=='POST':
        centercode = request.POST.get('centerCode')
        centername = request.POST.get('centerName')
        state = request.POST.get('state')
        place = request.POST.get('place')
        email = request.POST.get('emailId')
        contact = request.POST.get('contact')
        forsaving = addnewCenterlist(
            center_code = centercode,
            center_name = centername,
            state = state,
            place=place,
            email_id= email,
            contact=contact,
        ) 
        forsaving.save()  
    return redirect('adminhome')
    
    
