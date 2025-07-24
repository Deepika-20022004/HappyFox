# profile_builder/urls.py

from django.urls import path
from .views import ResumeCheckerView

urlpatterns = [
    path('check_resume/', ResumeCheckerView.as_view(), name='check-resume'),
]