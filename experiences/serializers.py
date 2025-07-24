from rest_framework import serializers
from django.contrib.auth.models import User
from .models import InterviewExperience, Comment

class AuthorSerializer(serializers.ModelSerializer):
    """
    A simple serializer to display user information without exposing sensitive data.
    """
    class Meta:
        model = User
        fields = ('id', 'username')

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    author = AuthorSerializer(read_only=True) # Nest the author's details

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at')
        read_only_fields = ('experience', 'author')

class InterviewExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for the InterviewExperience model. This is the main serializer.
    """
    author = AuthorSerializer(read_only=True)
    # Include all comments related to an experience, and make them read-only in this context.
    comments = CommentSerializer(many=True, read_only=True)
    # A field to show the total number of comments.
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)


    class Meta:
        model = InterviewExperience
        fields = (
            'id', 'author', 'company_name', 'role', 'experience_text',
            'verdict', 'created_at', 'comments', 'comments_count'
        )

    def create(self, validated_data):
        # When creating a new experience, we assign the logged-in user as the author.
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)