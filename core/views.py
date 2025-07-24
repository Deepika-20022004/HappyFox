from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from .models import CompanyDrive
from .serializers import CompanyDriveSerializer
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
            - "learning_goals" (a string of specific concepts to learn)
            - "suggested_resources" (a string of the 3 best valid links for the preparation")

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
            
            return Response(questions_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle potential errors from the AI API call or JSON parsing
            return Response(
                {'error': f'Failed to generate AI questions: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
