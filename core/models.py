from django.db import models
from django.utils import timezone

# Create your models here.

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    text_content = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} - {self.uploaded_at.strftime('%Y-%m-%d')}"

class JobApplication(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='job_applications')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_description = models.TextField()
    match_percentage = models.FloatField()
    missing_keywords = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.job_title} at {self.company} - {self.match_percentage}%"