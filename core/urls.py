from django.urls import path
from .views import *

urlpatterns = [
    path('companies/', CompanyDriveList.as_view(), name='company-list'),
    path('generate_prep_plan/', GeneratePreparationPlan.as_view(), name='generate-prep-plan'),
    path('generate_mock_interview/', MockInterviewGenerator.as_view(), name='generate-mock-interview'),
]