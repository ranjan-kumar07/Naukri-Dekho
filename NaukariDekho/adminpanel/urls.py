from django.urls import path
from . import views

urlpatterns = [

    # ==========================================
    # ADMIN DASHBOARD
    # ==========================================
    path(
        '',
        views.dashboard,
        name='admin_dashboard'
    ),

    # ==========================================
    # USERS MANAGEMENT
    # ==========================================
    path(
        'users/',
        views.users,
        name='admin_users'
    ),

    # ==========================================
    # ROLE MANAGEMENT (user / recruiter)
    # ==========================================
    path(
        'users/change-role/<int:profile_id>/<str:role>/',
        views.change_role,
        name='change_role'
    ),

    # ==========================================
    # ADMIN CONTROL
    # ==========================================
    path(
        'users/make-admin/<int:user_id>/',
        views.make_admin,
        name='make_admin'
    ),

    path(
        'users/remove-admin/<int:user_id>/',
        views.remove_admin,
        name='remove_admin'
    ),

    # ==========================================
    # DELETE USER
    # ==========================================
    path(
        'users/delete/<int:user_id>/',
        views.delete_user,
        name='delete_user'
    ),
    path('recruiters/', views.recruiters, name='admin_recruiters'),
    path('jobs/', views.jobs, name='admin_jobs'),
path('jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),

# APPLICATIONS
path(
    'applications/',
    views.applications,
    name='admin_applications'
),

path(
    'applications/status/<int:application_id>/<str:status>/',
    views.change_application_status,
    name='change_application_status'
),

path(
    'applications/delete/<int:application_id>/',
    views.delete_application,
    name='delete_application'
),
]