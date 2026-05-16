from django.urls import path
from . import views


urlpatterns = [

    # Home Page
    path(
        '',
        views.home,
        name='home'
    ),

    # All Jobs
    path(
        'jobs/',
        views.all_jobs,
        name='all_jobs'
    ),

    # Recruiter Dashboard
    path(
        'recruiter-dashboard/',
        views.recruiter_dashboard,
        name='recruiter_dashboard'
    ),

    # Add Job
    path(
        'add-job/',
        views.add_job,
        name='add_job'
    ),

    # Apply Job
    path(
        'apply-job/<int:job_id>/',
        views.apply_job,
        name='apply_job'
    ),

    # Posted Jobs
    path(
        'posted-jobs/',
        views.posted_jobs,
        name='posted_jobs'
    ),

    # Edit Job
    path(
        'edit-job/<int:job_id>/',
        views.edit_job,
        name='edit_job'
    ),

    # Delete Job
    path(
        'delete-job/<int:job_id>/',
        views.delete_job,
        name='delete_job'
    ),

    # Selected Applications
    path(
        'dashboard/selected/',
        views.selected_applications,
        name='selected_applications'
    ),

    # Update Application Status
    path(
        'update-application-status/<int:application_id>/<str:status>/',
        views.update_application_status,
        name='update_application_status'
    ),
]