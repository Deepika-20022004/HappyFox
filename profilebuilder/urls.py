# profile_builder/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('check_resume/', ResumeCheckerView.as_view(), name='check-resume'),
    path('register/', RegisterView.as_view(), name='register'),
]