from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend # Install: pip install django-filter
import random

class CompanyDriveList(generics.ListAPIView):
    queryset = CompanyDrive.objects.all().order_by('drive_date') # Default ordering
    serializer_class = CompanyDriveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'domain'] # Allow filtering by role and domain

class GeneratePreparationPlan(APIView):
    def post(self, request, *args, **kwargs):
        academic_course_details = request.data.get('academic_course_details', '')
        preferred_role = request.data.get('preferred_role', '').strip().lower()

        if not preferred_role:
            return Response({'error': 'Preferred role is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # --- Simple Logic for Plan Generation (Hackathon-Level AI) ---
        # This is where your "AI" logic goes. For a hackathon, it's rule-based.

        plan_details = {}
        recommendations = {}

        # 1. Infer core skills based on preferred role
        # This is a basic mapping. In a real scenario, you'd use a more robust lookup
        # or even NLP on role descriptions.
        role_to_skills = {
            'software engineer': ['Data Structures & Algorithms', 'System Design', 'Programming Language (e.g., Python/Java)', 'Operating Systems', 'Database Management Systems'],
            'data analyst': ['SQL', 'Excel', 'Statistics', 'Data Visualization', 'Python/R'],
            'associate consultant': ['Aptitude', 'Logical Reasoning', 'Communication Skills', 'Case Study'],
        }

        core_skills_for_role = role_to_skills.get(preferred_role, ['General Aptitude', 'Communication Skills'])

        plan_details['core_skills'] = []
        for skill_name in core_skills_for_role:
            plan_details['core_skills'].append({'name': skill_name, 'topics': []})

            # Fetch related topics for each skill
            try:
                skill_obj = Skill.objects.get(name=skill_name)
                topics_for_skill = PreparationTopic.objects.filter(associated_skills=skill_obj)

                for skill_dict in plan_details['core_skills']:
                    if skill_dict['name'] == skill_name:
                        for topic in topics_for_skill:
                            topic_data = {'name': topic.name, 'resources': []}
                            # Fetch resources for each topic
                            resources_for_topic = LearningResource.objects.filter(associated_topics=topic)
                            for res in resources_for_topic:
                                topic_data['resources'].append({'title': res.title, 'url': res.url, 'type': res.resource_type})
                            skill_dict['topics'].append(topic_data)
                        break
            except Skill.DoesNotExist:
                # Handle cases where a skill might not be seeded yet
                pass 

        # 2. Adjust based on academic context (very basic parsing)
        academic_adjustments = []
        if 'data structures' in academic_course_details.lower() or 'dsa' in academic_course_details.lower():
            academic_adjustments.append("Good! Keep practicing DSA. Focus on harder problems now.")
        if 'database' in academic_course_details.lower() or 'dbms' in academic_course_details.lower():
            academic_adjustments.append("Excellent! Leverage your DBMS knowledge for SQL/database specific roles.")

        if academic_adjustments:
            recommendations['academic_focus'] = academic_adjustments

        # 3. Basic time allocation estimate
        # For a hackathon, this is a fixed estimate
        recommendations['time_allocation'] = "Allocate 4-5 hours daily for focused preparation. Prioritize DSA and System Design."

        # 4. Consider remaining time (very basic based on next drive)
        next_drive = CompanyDrive.objects.order_by('drive_date').first()
        if next_drive:
            days_left = (next_drive.drive_date - date.today()).days
            if days_left > 0:
                recommendations['timeline_awareness'] = f"The nearest drive is in {days_left} days ({next_drive.company_name}). Structure your study plan effectively."
            else:
                recommendations['timeline_awareness'] = "Placement season is active! Focus on intensive preparation and mock interviews."
        else:
            recommendations['timeline_awareness'] = "No upcoming drives found. Continue building fundamental skills."
        
        return Response({
            'role': preferred_role,
            'academic_context': academic_course_details,
            'plan_details': plan_details,
            'recommendations': recommendations
        }, status=status.HTTP_200_OK)

class MockInterviewGenerator(APIView):
    def post(self, request, *args, **kwargs):
        company_id = request.data.get('company_id')
        role = request.data.get('role', '').strip().lower()
        num_questions = request.data.get('num_questions', 5) # Default to 5 questions

        questions = []

        # Filter questions based on company and role
        queryset = MockInterviewQuestion.objects.all()
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if role:
            queryset = queryset.filter(role__iexact=role) # Case-insensitive match

        # Simple strategy: try to get a mix of question types if available
        technical_questions = list(queryset.filter(question_type='technical'))
        behavioral_questions = list(queryset.filter(question_type='behavioral'))
        system_design_questions = list(queryset.filter(question_type='system_design'))
        aptitude_questions = list(queryset.filter(question_type='aptitude'))

        all_available_questions = list(queryset)

        # Prioritize a mix for variety in hackathon
        if len(technical_questions) >= num_questions * 0.4:
            questions.extend(random.sample(technical_questions, int(num_questions * 0.4)))
        else:
            questions.extend(technical_questions)

        remaining_slots = num_questions - len(questions)

        if remaining_slots > 0:
            if len(behavioral_questions) >= remaining_slots * 0.3:
                questions.extend(random.sample(behavioral_questions, int(remaining_slots * 0.3)))
            else:
                questions.extend(behavioral_questions)
            remaining_slots = num_questions - len(questions)

        if remaining_slots > 0:
             if len(system_design_questions) >= remaining_slots * 0.3:
                questions.extend(random.sample(system_design_questions, int(remaining_slots * 0.3)))
             else:
                questions.extend(system_design_questions)
             remaining_slots = num_questions - len(questions)

        # Fill remaining with any type if specific types are exhausted
        if remaining_slots > 0 and len(all_available_questions) > len(questions):
            # Ensure we don't pick duplicates if using all_available_questions
            unique_questions_ids = {q.id for q in questions}
            remaining_pool = [q for q in all_available_questions if q.id not in unique_questions_ids]
            questions.extend(random.sample(remaining_pool, min(remaining_slots, len(remaining_pool))))

        # Shuffle final list to mix types
        random.shuffle(questions)

        # Limit to num_questions requested
        final_questions = questions[:num_questions]

        serializer = MockInterviewQuestionSerializer(final_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
