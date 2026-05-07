from django.urls import path
from . import views

app_name = 'dashboard'  # Это важно!

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # name='dashboard'
]