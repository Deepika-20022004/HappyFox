from rest_framework import serializers
from .models import *

class CompanyDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDrive
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class PreparationTopicSerializer(serializers.ModelSerializer):
    associated_skills = SkillSerializer(many=True, read_only=True) # Nested serializer

    class Meta:
        model = PreparationTopic
        fields = '__all__'

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = '__all__'

# Serializer for the generated plan (not tied to a model)
class PreparationPlanSerializer(serializers.Serializer):
    # This describes the structure of the *output* plan
    role = serializers.CharField(max_length=255)
    academic_context = serializers.CharField()
    plan_details = serializers.JSONField() # Use JSONField to store structured plan content
    recommendations = serializers.JSONField()

class MockInterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockInterviewQuestion
        fields = '__all__'