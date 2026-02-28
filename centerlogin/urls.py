from django.urls import path
from centerlogin import views

urlpatterns = [
    path('center-dashboard/', views.cendashboard, name='cendashboard'),
    path('center-logout/', views.cenlogout, name='cenlogout'),
    path('center-entry-login/', views.entrylogin, name='entrylogin'),
    path('student-list/', views.studentlist, name='studentlist'),
    path('demo-center/', views.democenter, name='democenter'),
    path('cent-eremergency/', views.emergency, name='emergency'),
    path('cent-erarrange/', views.seatarr, name='arrange'),

    path('center/students/add/', views.add_student, name='center_add_student'),
    path('center/students/<int:student_id>/edit/', views.edit_student, name='center_edit_student'),
    path('center/students/<int:student_id>/delete/', views.delete_student, name='center_delete_student'),
    path('center/assignments/assign/', views.assign_exam, name='center_assign_exam'),
    path('center/assignments/<int:assignment_id>/update/', views.update_assignment, name='center_update_assignment'),
]
