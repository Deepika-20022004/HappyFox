from django.urls import path
from .views import (
    ExperienceListCreateView,
    ExperienceDetailView,
    CommentCreateView
)

urlpatterns = [
    # ex: /api/experiences/
    path('', ExperienceListCreateView.as_view(), name='experience-list-create'),
    # ex: /api/experiences/5/
    path('<int:pk>/', ExperienceDetailView.as_view(), name='experience-detail'),
    # ex: /api/experiences/5/comments/
    path('<int:experience_pk>/comments/', CommentCreateView.as_view(), name='comment-create'),
]