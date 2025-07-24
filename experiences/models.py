from django.db import models
from django.contrib.auth.models import User

class InterviewExperience(models.Model):
    VERDICT_CHOICES = [
        ('OFFERED', 'Offered'),
        ('REJECTED', 'Rejected'),
        ('WAITLISTED', 'Waitlisted'),
        ('NO_RESULT', 'No Result Yet'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    experience_text = models.TextField()
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES, default='NO_RESULT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}'s experience at {self.company_name} for {self.role}"

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    experience = models.ForeignKey(InterviewExperience, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.experience.id}"

    class Meta:
        ordering = ['created_at']