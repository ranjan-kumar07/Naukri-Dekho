from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'recruiter-dashboard/',
        views.recruiter_dashboard,
        name='recruiter_dashboard'
    ),

    path(
        'add-job/',
        views.add_job,
        name='add_job'
    ),

    

    path(
    'apply-job/<int:job_id>/',
    views.apply_job,
    name='apply_job'
),
    path(
    'posted-jobs/',
    views.posted_jobs,
    name='posted_jobs'
),

path(
    'jobs/',
    views.all_jobs,
    name='all_jobs'
),

]

