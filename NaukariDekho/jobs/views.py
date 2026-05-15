from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job, Application
from django.contrib import messages
from datetime import date
from .forms import ApplicationForm
from django.shortcuts import get_object_or_404

def home(request):

    return render(
        request,
        'home.html'
    )

@login_required
def add_job(request):

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.recruiter = request.user

            job.save()

            messages.success(
                request,
                'Job published successfully.'
            )

            return redirect('recruiter_dashboard')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = JobForm()

    context = {
        'form': form
    }

    return render(
        request,
        'recruiter/add_job.html',
        context
    )

# Recruiter Dashboard View


def recruiter_dashboard(request):

    jobs = Job.objects.filter(
        recruiter=request.user
    )

    applications = Application.objects.filter(
        job__recruiter=request.user
    )

    accepted_count = applications.filter(
        status='accepted'
    ).count()

    context = {

        'jobs': jobs,

        'applications': applications,

        'accepted_count': accepted_count,

    }

    return render(
        request,
        'recruiter/recruiter_dashboard.html',
        context
    )

# user job list 

def jobs_list(request):

    jobs = Job.objects.filter(
        application_deadline__gte=date.today()
    ).order_by('-created_at')

    context = {
        'jobs': jobs
    }

    return render(
        request,
        'user/jobs_list.html',
        context
    )

# job apply view




@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    # Check if already applied
    already_applied = Application.objects.filter(
        user=request.user,
        job=job
    ).exists()

    if already_applied:

        messages.warning(
            request,
            'You have already applied for this job.'
        )

        return redirect('user_dashboard')

    form = ApplicationForm()

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(commit=False)

            application.user = request.user
            application.job = job

            application.save()

            # Success Message
            messages.success(
                request,
                'Application submitted successfully!'
            )

            return redirect('user_dashboard')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    context = {

        'job': job,
        'form': form

    }

    return render(
        request,
        'user/apply_job.html',
        context
    )

@login_required
def posted_jobs(request):

    jobs = Job.objects.filter(
        recruiter=request.user
    )

    context = {
        'jobs': jobs
    }

    return render(
        request,
        'recruiter/posted_jobs.html',
        context
    )

from accounts.models import Profile

def all_jobs(request):

    jobs = Job.objects.filter(
        application_deadline__gte=date.today()
    )

    role = None

    if request.user.is_authenticated:

        profile = Profile.objects.filter(
            user=request.user
        ).first()

        if profile:
            role = profile.role

    context = {
        'jobs': jobs,
        'role': role
    }

    return render(
        request,
        'all_jobs.html',
        context
    )

# job edit view

@login_required
def edit_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    if request.method == 'POST':

        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Job updated successfully.'
            )

            return redirect('posted_jobs')

    else:

        form = JobForm(instance=job)

    context = {
        'form': form,
        'is_edit': True,
    }

    return render(
        request,
        'recruiter/edit_job.html',
        context
    )

# job delete view
@login_required
def delete_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    job.delete()

    messages.success(
        request,
        'Job deleted successfully.'
    )

    return redirect('posted_jobs')


# users selected applications 
@login_required
def selected_applications(request):
    # Fetch applications where the status is accepted/selected for this user
    successful_apps = Application.objects.filter(
        user=request.user, 
        status='Selected' # <--- Match your model's status choices (e.g., 'Accepted')
    ).select_related('job') # Optimizes database query for job details
    
    return render(request, 'user/selected_applications.html', {
        'applications': successful_apps
    })