from django.db import models


class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.department}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Extracted fields from resume via Groq AI
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=200, blank=True)
    current_role = models.CharField(max_length=200, blank=True)
    years_of_experience = models.CharField(max_length=50, blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    extraction_successful = models.BooleanField(default=False)
    raw_extracted_text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name or 'Unknown'} -> {self.position or 'General'} ({self.applied_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-applied_at']
