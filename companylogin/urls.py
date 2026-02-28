from django.urls import path
from companylogin import views

urlpatterns=[
    path('com_dashboard/',views.com_dashboard,name="com_dashboard"),
    path('addexam/',views.addExam,name="addexam"),
    path('ongoingtests/',views.ongoing_tests,name="ongoingtests"),
    path('completedtests/',views.completed_tests,name="completedtests"),
    path('centers/',views.centers,name="centers"),
    path('addcenter/',views.addCenter,name="addcenter"),
    path('saveexam/',views.saveExam,name="saveexam"),
    path('logout/',views.comLogout,name="logout"),
    path('company-entry/',views.companyentry,name="companyentry"),
    path('password-center/',views.passcenter,name="passcenter"),
    path('questions/',views.questions,name="questions"),
    path('addquestion/',views.addQuestion,name="addquestion"),
    path('ai/generate-questions/', views.generate_ai_questions, name="ai_generate_questions"),
    path('ai/save-questions/', views.save_ai_questions, name="ai_save_questions"),
    
]
