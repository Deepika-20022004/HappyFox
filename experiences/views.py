# experiences/views.py

from rest_framework import generics, permissions
from .models import InterviewExperience, Comment
from .serializers import InterviewExperienceSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly # We will create this custom permission

class ExperienceListCreateView(generics.ListCreateAPIView):
    """
    View to list all interview experiences or create a new one.
    - GET: Returns a list of all experiences.
    - POST: Creates a new experience. User must be authenticated.
    """
    queryset = InterviewExperience.objects.all()
    serializer_class = InterviewExperienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Only logged-in users can post.

class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a single interview experience.
    - GET: Returns a single experience by its ID.
    - PUT/PATCH: Updates an experience. User must be the author.
    - DELETE: Deletes an experience. User must be the author.
    """
    queryset = InterviewExperience.objects.all()
    serializer_class = InterviewExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly] # Custom permission to ensure only author can edit.

class CommentCreateView(generics.CreateAPIView):
    """
    View to create a new comment for a specific interview experience.
    - POST: Creates a new comment. User must be authenticated.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the author and the related experience post.
        experience = InterviewExperience.objects.get(pk=self.kwargs['experience_pk'])
        serializer.save(author=self.request.user, experience=experience)