from django.db import models

# Module 1
class CompanyDrive(models.Model):
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    hiring_timeline = models.CharField(max_length=255, help_text="e.g., 'August 2025', 'Q3 2025'")
    drive_date = models.DateField(help_text="Primary date for ordering drives")
    location = models.CharField(max_length=255, blank=True, null=True)
    interview_process_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.role} ({self.drive_date})"

# Module 2
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PreparationTopic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Many-to-many relationship with Skill
    associated_skills = models.ManyToManyField(Skill, related_name='prep_topics')

    def __str__(self):
        return self.name

class LearningResource(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    resource_type = models.CharField(max_length=50, choices=[('video', 'Video'), ('article', 'Article'), ('course', 'Course'), ('problem', 'Problem Set')])
    # Many-to-many with PreparationTopic
    associated_topics = models.ManyToManyField(PreparationTopic, related_name='resources')

    def __str__(self):
        return self.title
    
# Module 3
class MockInterviewQuestion(models.Model):
    # Link to a specific company or keep general
    company = models.ForeignKey(CompanyDrive, on_delete=models.SET_NULL, null=True, blank=True,
                                help_text="Optional: company this question is specific to")
    role = models.CharField(max_length=100, help_text="e.g., Software Engineer, Data Analyst")
    question_text = models.TextField()
    difficulty_level = models.CharField(max_length=50, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    question_type = models.CharField(max_length=50, choices=[('technical', 'Technical'), ('behavioral', 'Behavioral'), ('system_design', 'System Design'), ('aptitude', 'Aptitude')], default='technical')
    expected_answer_keywords = models.TextField(blank=True, help_text="Comma-separated keywords for basic assessment")
    sample_answer = models.TextField(blank=True, help_text="A model answer for reference")

    def __str__(self):
        return f"Mock Q for {self.role} ({self.company.company_name if self.company else 'General'}) - {self.question_type}"