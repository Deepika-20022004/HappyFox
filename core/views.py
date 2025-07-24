from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend # Install: pip install django-filter
import random

# For integrating AI
import os
import google.generativeai as genai
import json

class CompanyDriveList(generics.ListAPIView):
    queryset = CompanyDrive.objects.all().order_by('drive_date') # Default ordering
    serializer_class = CompanyDriveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'domain'] # Allow filtering by role and domain

class GeneratePreparationPlan(APIView):
    # For integrating AI

    def post(self, request, *args, **kwargs):
        # 1. Gather detailed inputs from the user's request
        course_details = request.data.get('course_details')
        preferred_role = request.data.get('preferred_role')
        current_skills = request.data.get('current_skills') # e.g., "Python, Java, DSA Basics"
        timeframe_weeks = int(request.data.get('timeframe_weeks', 8))

        # Basic validation
        if not all([course_details, preferred_role, current_skills]):
            return Response(
                {'error': 'Missing required fields: course_details, preferred_role, current_skills are all required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 2. Configure the Gemini API client
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')

            # 3. Craft a highly detailed prompt for a structured study plan
            prompt = f"""
            You are an expert career and placement coach from a top-tier Indian engineering college (like an IIT or NIT). Your task is to create a hyper-personalized, week-by-week study plan for a student.

            The plan must prioritize bridging the gap between the student's known skills and the requirements of their target role, using their strengths as a foundation.

            **Student Profile:**
            - **Course:** {course_details}
            - **Target Role:** {preferred_role}
            - **Current Strengths / Known Skills:** {current_skills}
            - **Preparation Timeframe:** {timeframe_weeks} weeks

            **Output Requirements:**
            The output MUST be a valid, compact, single-line JSON object.
            This object must contain a single key: "weekly_plan".
            "weekly_plan" must be a list of objects, where each object represents one week and contains the following keys:
            - "week" (string, e.g., "Week 1")
            - "milestone" (string, a one-sentence summary of the week's main goal, e.g., "Mastering Advanced Array Manipulations.")
            - "topic_focus" (string, the primary technical domain for the week, e.g., "Data Structures and Algorithms")
            - "learning_goals" (a JSON array of strings detailing specific concepts to learn)
            - "suggested_resources" (a JSON array of strings of the 3 best valid links for the preparation")

            Ensure the plan is realistic, logically progressive, and directly tailored to the student's profile.
            """

            # 4. Call the AI model and parse the response robustly
            response = model.generate_content(prompt)
            clean_json_text = response.text.replace('```json', '').replace('```', '').strip()
            parsable_text = clean_json_text.replace('\n', '\\n')
            plan_data = json.loads(parsable_text)

            # 5. Send the structured plan to the frontend
            return Response(plan_data, status=status.HTTP_200_OK)

        except json.JSONDecodeError as e:
            return Response(
                {'error': f'Failed to parse AI response as JSON: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # def post(self, request, *args, **kwargs):
    #     academic_course_details = request.data.get('academic_course_details', '')
    #     preferred_role = request.data.get('preferred_role', '').strip().lower()

    #     if not preferred_role:
    #         return Response({'error': 'Preferred role is required.'}, status=status.HTTP_400_BAD_REQUEST)

    #     plan_details = {}
    #     recommendations = {}

    #     # 1. Infer core skills based on preferred role
    #     # This is a basic mapping. In a real scenario, you'd use a more robust lookup
    #     # or even NLP on role descriptions.
    #     role_to_skills = {
    #         'software engineer': ['Data Structures & Algorithms', 'System Design', 'Programming Language (e.g., Python/Java)', 'Operating Systems', 'Database Management Systems'],
    #         'data analyst': ['SQL', 'Excel', 'Statistics', 'Data Visualization', 'Python/R'],
    #         'associate consultant': ['Aptitude', 'Logical Reasoning', 'Communication Skills', 'Case Study'],
    #     }

    #     core_skills_for_role = role_to_skills.get(preferred_role, ['General Aptitude', 'Communication Skills'])

    #     plan_details['core_skills'] = []
    #     for skill_name in core_skills_for_role:
    #         plan_details['core_skills'].append({'name': skill_name, 'topics': []})

    #         # Fetch related topics for each skill
    #         try:
    #             skill_obj = Skill.objects.get(name=skill_name)
    #             topics_for_skill = PreparationTopic.objects.filter(associated_skills=skill_obj)

    #             for skill_dict in plan_details['core_skills']:
    #                 if skill_dict['name'] == skill_name:
    #                     for topic in topics_for_skill:
    #                         topic_data = {'name': topic.name, 'resources': []}
    #                         # Fetch resources for each topic
    #                         resources_for_topic = LearningResource.objects.filter(associated_topics=topic)
    #                         for res in resources_for_topic:
    #                             topic_data['resources'].append({'title': res.title, 'url': res.url, 'type': res.resource_type})
    #                         skill_dict['topics'].append(topic_data)
    #                     break
    #         except Skill.DoesNotExist:
    #             # Handle cases where a skill might not be seeded yet
    #             pass 

    #     # 2. Adjust based on academic context (very basic parsing)
    #     academic_adjustments = []
    #     if 'data structures' in academic_course_details.lower() or 'dsa' in academic_course_details.lower():
    #         academic_adjustments.append("Good! Keep practicing DSA. Focus on harder problems now.")
    #     if 'database' in academic_course_details.lower() or 'dbms' in academic_course_details.lower():
    #         academic_adjustments.append("Excellent! Leverage your DBMS knowledge for SQL/database specific roles.")

    #     if academic_adjustments:
    #         recommendations['academic_focus'] = academic_adjustments

    #     # 3. Basic time allocation estimate
    #     # For a hackathon, this is a fixed estimate
    #     recommendations['time_allocation'] = "Allocate 4-5 hours daily for focused preparation. Prioritize DSA and System Design."

    #     # 4. Consider remaining time (very basic based on next drive)
    #     next_drive = CompanyDrive.objects.order_by('drive_date').first()
    #     if next_drive:
    #         days_left = (next_drive.drive_date - date.today()).days
    #         if days_left > 0:
    #             recommendations['timeline_awareness'] = f"The nearest drive is in {days_left} days ({next_drive.company_name}). Structure your study plan effectively."
    #         else:
    #             recommendations['timeline_awareness'] = "Placement season is active! Focus on intensive preparation and mock interviews."
    #     else:
    #         recommendations['timeline_awareness'] = "No upcoming drives found. Continue building fundamental skills."
        
    #     return Response({
    #         'role': preferred_role,
    #         'academic_context': academic_course_details,
    #         'plan_details': plan_details,
    #         'recommendations': recommendations
    #     }, status=status.HTTP_200_OK)


class MockInterviewGenerator(APIView):
    # For integrating AI
    def post(self, request, *args, **kwargs):
        company_id = request.data.get('company_id')
        role = request.data.get('role', '').strip()
        num_questions = int(request.data.get('num_questions', 10))

        if not role or not company_id:
            return Response(
                {'error': 'Company and role are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch company name from the database using the ID
            company = CompanyDrive.objects.get(id=company_id)
            company_name = company.company_name
        except CompanyDrive.DoesNotExist:
            return Response(
                {'error': 'Company not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # --- AI Integration Logic ---
        try:
            # Configure the Gemini API client
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Create a detailed prompt for the AI
            prompt = f"""
            Act as an expert technical interviewer at "{company_name}".
            Generate a realistic mock interview question set for a "{role}" candidate.
            The output must be a valid, compact, single-line JSON list of exactly {num_questions} questions.

            Each JSON object in the list must have the following keys:
            - "question_text": The interview question.
            - "question_type": The type of question (must be one of: 'technical', 'behavioral', 'system_design', 'aptitude').
            - "difficulty_level": The difficulty (must be one of: 'easy', 'medium', 'hard').
            - "sample_answer": A detailed, high-quality model answer for the question.
            - "expected_answer_keywords": A comma-separated string of important keywords.

            Ensure all string values in the JSON are properly escaped.
            """

            # Call the AI model
            response = model.generate_content(prompt)

            # Clean and parse the response
            clean_json_text = response.text.replace('```json', '').replace('```', '').strip()
            questions_data = json.loads(clean_json_text)
            
            # Since the data is not from our DB, it won't have an 'id', which is fine
            # for the frontend if it's handled correctly. We can also add a temporary one.
            for i, q in enumerate(questions_data):
                q['id'] = i + 1
                q['company'] = company_id # Add company ID for consistency
                q['role'] = role # Add role for consistency


            # We can still use our serializer to validate the structure if we want,
            # but it's not strictly necessary if the prompt is good.
            serializer = MockInterviewQuestionSerializer(data=questions_data, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If AI gives bad data, fall back to DB or show error
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Handle potential errors from the AI API call or JSON parsing
            return Response(
                {'error': f'Failed to generate AI questions: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Without AI

    # def post(self, request, *args, **kwargs):
    #     company_id = request.data.get('company_id')
    #     role = request.data.get('role', '').strip().lower()
    #     num_questions = request.data.get('num_questions', 5) # Default to 5 questions

    #     questions = []

    #     # Filter questions based on company and role
    #     queryset = MockInterviewQuestion.objects.all()
    #     if company_id:
    #         queryset = queryset.filter(company_id=company_id)
    #     if role:
    #         queryset = queryset.filter(role__iexact=role) # Case-insensitive match

    #     # Simple strategy: try to get a mix of question types if available
    #     technical_questions = list(queryset.filter(question_type='technical'))
    #     behavioral_questions = list(queryset.filter(question_type='behavioral'))
    #     system_design_questions = list(queryset.filter(question_type='system_design'))
    #     aptitude_questions = list(queryset.filter(question_type='aptitude'))

    #     all_available_questions = list(queryset)

    #     # Prioritize a mix for variety in hackathon
    #     if len(technical_questions) >= num_questions * 0.4:
    #         questions.extend(random.sample(technical_questions, int(num_questions * 0.4)))
    #     else:
    #         questions.extend(technical_questions)

    #     remaining_slots = num_questions - len(questions)

    #     if remaining_slots > 0:
    #         if len(behavioral_questions) >= remaining_slots * 0.3:
    #             questions.extend(random.sample(behavioral_questions, int(remaining_slots * 0.3)))
    #         else:
    #             questions.extend(behavioral_questions)
    #         remaining_slots = num_questions - len(questions)

    #     if remaining_slots > 0:
    #          if len(system_design_questions) >= remaining_slots * 0.3:
    #             questions.extend(random.sample(system_design_questions, int(remaining_slots * 0.3)))
    #          else:
    #             questions.extend(system_design_questions)
    #          remaining_slots = num_questions - len(questions)

    #     # Fill remaining with any type if specific types are exhausted
    #     if remaining_slots > 0 and len(all_available_questions) > len(questions):
    #         # Ensure we don't pick duplicates if using all_available_questions
    #         unique_questions_ids = {q.id for q in questions}
    #         remaining_pool = [q for q in all_available_questions if q.id not in unique_questions_ids]
    #         questions.extend(random.sample(remaining_pool, min(remaining_slots, len(remaining_pool))))

    #     # Shuffle final list to mix types
    #     random.shuffle(questions)

    #     # Limit to num_questions requested
    #     final_questions = questions[:num_questions]

    #     serializer = MockInterviewQuestionSerializer(final_questions, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
