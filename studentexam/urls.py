from django.urls import path
from studentexam import views
urlpatterns=[
    path('student-home/',views.studhome,name="studhome"),
    path('instruction/',views.instruction,name="instruction"),
    path('running-exam/',views.running,name="running"),
    path('exam-over/',views.over,name="over"),
    path('get_next_question/<int:current_question_id>/', views.get_next_question, name='get_next_question'),
    path('get_previous_question/<int:current_question_id>/', views.get_previous_question, name='get_previous_question'),
]
