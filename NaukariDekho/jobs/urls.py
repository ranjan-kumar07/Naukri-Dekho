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
path(
    'edit-job/<int:job_id>/',
    views.edit_job,
    name='edit_job'
),

path(
    'delete-job/<int:job_id>/',
    views.delete_job,
    name='delete_job'
),
path('dashboard/selected/', views.selected_applications, name='selected_applications'),

]

