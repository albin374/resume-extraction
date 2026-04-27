import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import JobApplication, JobPosition
from .forms import JobApplicationForm
from .utils import process_resume


def apply_job(request):
    positions = JobPosition.objects.filter(is_active=True)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.save()

            # Process resume PDF
            pdf_path = application.resume.path
            data, error = process_resume(pdf_path)

            if data:
                application.full_name = data.get('full_name', '')
                application.email = data.get('email', '')
                application.phone = data.get('phone', '')
                application.location = data.get('location', '')
                application.current_role = data.get('current_role', '')
                application.years_of_experience = data.get('years_of_experience', '')
                application.skills = data.get('skills', '')
                application.education = data.get('education', '')
                application.work_experience = data.get('work_experience', '')
                application.summary = data.get('summary', '')
                application.linkedin = data.get('linkedin', '')
                application.github = data.get('github', '')
                application.raw_extracted_text = data.get('raw_text', '')
                application.extraction_successful = True
                application.save()
                messages.success(request, f"Application submitted! We extracted your details automatically.")
            else:
                application.extraction_successful = False
                application.save()
                messages.warning(request, f"Resume uploaded but data extraction had issues: {error}")

            return redirect('application_success', pk=application.pk)
    else:
        form = JobApplicationForm()

    return render(request, 'onboarding/apply.html', {'form': form, 'positions': positions})


def application_success(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'onboarding/success.html', {'application': application})


# ---- Admin Views ----

def admin_dashboard(request):
    applications = JobApplication.objects.select_related('position').all()

    # Filter
    status_filter = request.GET.get('status', '')
    position_filter = request.GET.get('position', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    if position_filter:
        applications = applications.filter(position_id=position_filter)

    positions = JobPosition.objects.all()
    stats = {
        'total': JobApplication.objects.count(),
        'pending': JobApplication.objects.filter(status='pending').count(),
        'shortlisted': JobApplication.objects.filter(status='shortlisted').count(),
        'hired': JobApplication.objects.filter(status='hired').count(),
    }

    return render(request, 'onboarding/admin_dashboard.html', {
        'applications': applications,
        'positions': positions,
        'stats': stats,
        'status_filter': status_filter,
        'position_filter': position_filter,
        'status_choices': JobApplication.STATUS_CHOICES,
    })


def admin_application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f"Status updated to {application.get_status_display()}")
            return redirect('admin_application_detail', pk=pk)

    return render(request, 'onboarding/admin_detail.html', {'application': application})


def update_status(request, pk):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            return JsonResponse({'success': True, 'status': application.get_status_display()})
    return JsonResponse({'success': False})
