# profile_builder/views.py

import os
import io
import re
import json
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

# (This is the full "Code 2" from the prompt)
class ResumeCheckerView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        job_description_text = request.data.get('job_description_text', '')
        resume_file = request.FILES.get('resume_file')

        if not resume_file or not job_description_text:
            return Response(
                {"error": "Both resume file and job description text are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract text from resume file
        resume_text = self._extract_text_from_file(resume_file)

        if isinstance(resume_text, Response):  # Error response
            return resume_text

        # Check if Gemini API is available
        gemini_api_key = os.environ.get('GEMINI_API_KEY')

        if gemini_api_key:
            try:
                return self._analyze_with_gemini(resume_text, job_description_text)
            except Exception as e:
                print(f"Gemini API error: {e}")
                # Fall back to basic analysis
                return self._analyze_with_fallback(resume_text, job_description_text)
        else:
            # Use fallback analysis
            return self._analyze_with_fallback(resume_text, job_description_text)

    def _extract_text_from_file(self, resume_file):
        """Extract text from uploaded resume file"""
        resume_text = ""
        file_extension = resume_file.name.split('.')[-1].lower()

        try:
            if file_extension == 'pdf':
                reader = PdfReader(io.BytesIO(resume_file.read()))
                for page in reader.pages:
                    resume_text += page.extract_text() or ''
            elif file_extension == 'docx':
                document = Document(io.BytesIO(resume_file.read()))
                for para in document.paragraphs:
                    resume_text += para.text + '\n'
            elif file_extension == 'txt':
                resume_text = resume_file.read().decode('utf-8')
            else:
                return Response(
                    {"error": "Unsupported file format. Please upload a PDF, DOCX, or TXT file."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(f"Error processing resume file: {e}")
            return Response(
                {"error": "Could not process resume file. Please ensure it's a valid and readable PDF/DOCX/TXT file.", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not resume_text.strip():
            return Response(
                {"error": "Could not extract readable text from the resume file. Please try a different file or format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return resume_text

    def _analyze_with_gemini(self, resume_text, job_description_text):
        """Analyze resume using Gemini AI"""
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash') 

        prompt = self._create_resume_analysis_prompt(resume_text, job_description_text)

        response = model.generate_content(prompt)
        gemini_response = response.text

        # Parse the Gemini response
        analysis_result = self._parse_gemini_analysis_response(gemini_response, resume_text, job_description_text)

        return Response(analysis_result, status=status.HTTP_200_OK)

    def _create_resume_analysis_prompt(self, resume_text, job_description_text):
        """Create a structured prompt for Gemini AI resume analysis"""
        # This is the detailed prompt from Code 2
        return f"""
        You are an expert ATS (Applicant Tracking System) and career coach. Analyze the following resume against the job description and provide comprehensive feedback.

        RESUME TEXT:
        {resume_text}

        JOB DESCRIPTION:
        {job_description_text}

        Please provide your analysis in the following JSON format:
        {{
            "overall_match_score": "X/10 - Brief explanation",
            "ats_compatibility_score": "X/10 - Brief explanation on formatting and keywords",
            "matched_keywords": ["keyword1", "keyword2"],
            "missing_important_keywords": ["missing_keyword1", "missing_keyword2"],
            "resume_strengths": ["Strength 1 with specific example", "Strength 2"],
            "improvement_suggestions": [
                {{"category": "Keywords & Skills", "suggestions": ["Specific suggestion 1"]}},
                {{"category": "Experience & Achievements", "suggestions": ["Specific suggestion 1"]}},
                {{"category": "Formatting & Structure", "suggestions": ["Specific suggestion 1"]}}
            ],
            "action_items": ["Immediate action 1", "Immediate action 2"]
        }}

        Focus on:
        1. ATS optimization and keyword matching.
        2. Relevance to the specific job requirements.
        3. Quantifiable achievements and impact statements.
        4. Technical skills alignment.
        5. Resume structure and formatting for ATS compatibility.

        Ensure your response contains valid JSON only, starting with {{ and ending with }}.
        """

    def _parse_gemini_analysis_response(self, gemini_response, resume_text, job_description_text):
        """Parse Gemini's analysis response and format it"""
        try:
            # Clean the response to extract only the JSON part
            json_match = re.search(r'\{.*\}', gemini_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # If no JSON is found, fall back
                print("Gemini did not return valid JSON, falling back to basic analysis.")
                return self._analyze_with_fallback(resume_text, job_description_text).data
        except Exception as e:
            print(f"Error parsing Gemini analysis response: {e}")
            # Fallback if parsing fails
            return self._analyze_with_fallback(resume_text, job_description_text).data


    def _analyze_with_fallback(self, resume_text, job_description_text):
        """Fallback analysis using basic keyword matching"""
        # (This is the fallback analysis code from Code 2)
        # For brevity, this part is assumed to be the same as in the prompt.
        # This function provides a basic response if the AI fails.
        resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
        job_words = set(re.findall(r'\b\w+\b', job_description_text.lower()))
        common_words = {'and', 'the', 'is', 'in', 'a', 'to', 'with', 'for', 'of', 'on'}
        job_keywords = {word for word in job_words if word not in common_words and len(word) > 2}

        matching_keywords = list(resume_words.intersection(job_keywords))
        missing_keywords = list(job_keywords.difference(resume_words))

        score = (len(matching_keywords) / len(job_keywords)) * 100 if len(job_keywords) > 0 else 0

        return Response({
            "overall_match_score": f"{round(score)}% Keyword Match",
            "ats_compatibility_score": "N/A (Basic Analysis)",
            "matched_keywords": matching_keywords,
            "missing_important_keywords": missing_keywords,
            "resume_strengths": ["This is a fallback analysis based on keyword matching."],
            "improvement_suggestions": [{"category": "General", "suggestions": ["The AI analysis failed. Please check your keywords against the job description manually."]}],
            "action_items": ["Review the matched and missing keywords."],
            "disclaimer": "AI analysis failed. This is a basic keyword-matching result."
        }, status=status.HTTP_200_OK)