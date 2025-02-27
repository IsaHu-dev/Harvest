from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"), 
    path('my-logout', views.my_login, name="my-logout"), 
    path('user-logout', views.user_logout, name="user-logout"), 
    # ✅ Fixed Password Reset URLs
]





