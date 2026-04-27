from django import forms
from .models import JobApplication, JobPosition


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['position', 'resume']
        widgets = {
            'position': forms.Select(attrs={
                'class': 'form-select',
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
            }),
        }
        labels = {
            'position': 'Applying for Position',
            'resume': 'Upload Resume (PDF only)',
        }
