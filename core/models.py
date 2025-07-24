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