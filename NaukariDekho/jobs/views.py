from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from datetime import date

from .forms import JobForm, ApplicationForm

from .models import Job, Application

from accounts.models import Profile


# Home View
def home(request):

    return render(
        request,
        'home.html'
    )


# Add Job View
@login_required
def add_job(request):

    if request.method == 'POST':

        form = JobForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            job = form.save(commit=False)

            job.recruiter = request.user

            job.save()

            messages.success(
                request,
                'Job published successfully.'
            )

            return redirect(
                'recruiter_dashboard'
            )

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


# Recruiter Dashboard
@login_required
def recruiter_dashboard(request):

    jobs = Job.objects.filter(
        recruiter=request.user
    ).order_by('-created_at')

    applications = Application.objects.filter(
        job__recruiter=request.user
    ).select_related(
        'user',
        'job'
    ).order_by('-applied_at')

    accepted_count = applications.filter(
        status='accepted'
    ).count()

    shortlisted_count = applications.filter(
        status='shortlisted'
    ).count()

    reviewing_count = applications.filter(
        status='reviewing'
    ).count()

    context = {

        'jobs': jobs,

        'applications': applications,

        'accepted_count': accepted_count,

        'shortlisted_count': shortlisted_count,

        'reviewing_count': reviewing_count,
    }

    return render(
        request,
        'recruiter/recruiter_dashboard.html',
        context
    )


# User Jobs List
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


# Apply Job View
@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    # Check duplicate application
    already_applied = Application.objects.filter(
        user=request.user,
        job=job
    ).exists()

    if already_applied:

        messages.warning(
            request,
            'You have already applied for this job.'
        )

        return redirect(
            'user_dashboard'
        )

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.user = request.user

            application.job = job

            # Default status
            application.status = 'applied'

            application.save()

            messages.success(
                request,
                'Application submitted successfully!'
            )

            return redirect(
                'user_dashboard'
            )

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = ApplicationForm()

    context = {

        'job': job,

        'form': form
    }

    return render(
        request,
        'user/apply_job.html',
        context
    )


# Posted Jobs View
@login_required
def posted_jobs(request):

    jobs = Job.objects.filter(
        recruiter=request.user
    ).order_by('-created_at')

    context = {
        'jobs': jobs
    }

    return render(
        request,
        'recruiter/posted_jobs.html',
        context
    )


# All Jobs View
def all_jobs(request):

    jobs = Job.objects.filter(
        application_deadline__gte=date.today()
    ).order_by('-created_at')

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


# Edit Job View
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
            request.FILES,
            instance=job
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Job updated successfully.'
            )

            return redirect(
                'posted_jobs'
            )

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = JobForm(
            instance=job
        )

    context = {

        'form': form,

        'is_edit': True,
    }

    return render(
        request,
        'recruiter/edit_job.html',
        context
    )


# Delete Job View
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

    return redirect(
        'posted_jobs'
    )


# Selected Applications View
@login_required
def selected_applications(request):

    successful_apps = Application.objects.filter(
        user=request.user,
        status='accepted'
    ).select_related(
        'job'
    ).order_by('-updated_at')

    return render(
        request,
        'user/selected_applications.html',
        {
            'applications': successful_apps
        }
    )


# Update Application Status
@login_required
def update_application_status(
    request,
    application_id,
    status
):

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=request.user
    )

    valid_statuses = [
        'reviewing',
        'shortlisted',
        'accepted',
        'rejected'
    ]

    if status in valid_statuses:

        application.status = status

        application.save()

        messages.success(
            request,
            f'Application status updated to {status}.'
        )

    else:

        messages.error(
            request,
            'Invalid status.'
        )

    return redirect(
        'recruiter_dashboard'
    )

def about(request):

    return render(
        request,
        'about.html'
    )


def contact(request):

    return render(
        request,
        'contact.html'
    )