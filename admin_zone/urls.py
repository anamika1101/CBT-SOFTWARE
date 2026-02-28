from django.urls import path
from admin_zone import views

urlpatterns = [
    path('adminhome/',views.admin_home,name = "adminhome"),
    path('adminlogout/',views.admin_logout,name = "adminlogout"),
    path('addcenter/',views.add_center,name = "addcenter"),
]