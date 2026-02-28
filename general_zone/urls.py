from django.urls import include, path
from general_zone import views
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet


router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('comsignup/', views.comsignup, name="comsignup"),
    path('comlogin/', views.comLogin, name="comlogin"),
    path('centerlogin/', views.centerlogin, name="centerlogin"),
    path('adminlogin/', views.admin_login, name="adminlogin"),

    # Public pages
    path('about/', views.about, name="about"),
    path('services/', views.services, name="services"),
    path('courses/', views.courses, name="courses"),
    path('homepage-centerlist/', views.centerlist, name="centerlist"),
    path('requestdemo/', views.request_demo, name="requestdemo"),

    # Role-based login landing pages
    path('login/company/', views.company_login_page, name='company_login_page'),
    path('signup/company/', views.company_signup_page, name='company_signup_page'),
    path('login/admin/', views.admin_login_page, name='admin_login_page'),
    path('login/center/', views.center_login_page, name='center_login_page'),
    path('signup/center/', views.center_signup_page, name='center_signup_page'),
    path('login/student/', views.student_login_page, name='student_login_page'),

    # Dashboard previews - show role capabilities
    path('dashboard/company/', views.company_dashboard_preview, name='company_dashboard_preview'),
    path('dashboard/center/', views.center_dashboard_preview, name='center_dashboard_preview'),
    path('dashboard/admin/', views.admin_dashboard_preview, name='admin_dashboard_preview'),

    # Logout routes
    path('logout/company/', views.company_logout, name='company_logout'),
    path('logout/center/', views.center_logout, name='center_logout'),
    path('logout/admin/', views.admin_logout, name='admin_logout'),

    path('', include(router.urls)),
]
