from django.urls import path, include
from . import views

urlpatterns = [
    path('registeration/', views.registeration, name='registeration'),
]