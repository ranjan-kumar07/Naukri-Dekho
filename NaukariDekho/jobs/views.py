from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job, Application
from django.contrib import messages


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

    jobs = Job.objects.all().order_by('-created_at')

    context = {
        'jobs': jobs
    }

    return render(
        request,
        'user/jobs_list.html',
        context
    )

# job apply view


from .forms import ApplicationForm
from django.shortcuts import get_object_or_404

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

    jobs = Job.objects.all()

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