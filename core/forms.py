from django import forms
from .models import Resume, JobApplication


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job_title', 'company', 'location', 'job_description']
        widgets = {
            'job_description': forms.Textarea(attrs={'rows': 10}),
        }
