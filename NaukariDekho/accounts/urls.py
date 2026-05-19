from django.urls import path

from . import views


urlpatterns = [

    # ==========================================
    # AUTHENTICATION
    # ==========================================

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # ==========================================
    # DASHBOARDS
    # ==========================================

    path(
        'user-dashboard/',
        views.user_dashboard,
        name='user_dashboard'
    ),

    path(
        'recruiter-dashboard/',
        views.recruiter_dashboard,
        name='recruiter_dashboard'
    ),

    # ==========================================
    # PROFILE
    # ==========================================

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

    path(
        'update-profile/',
        views.edit_profile,
        name='update_profile'
    ),

    # ==========================================
    # SKILLS
    # ==========================================

    path(
        'add-skill/',
        views.add_skill,
        name='add_skill'
    ),

    # ==========================================
    # EDUCATION
    # ==========================================

    path(
        'add-education/',
        views.add_education,
        name='add_education'
    ),

    # ==========================================
    # EXPERIENCE
    # ==========================================

    path(
        'add-experience/',
        views.add_experience,
        name='add_experience'
    ),

    # ==========================================
    # PROJECTS
    # ==========================================

    path(
        'add-project/',
        views.add_project,
        name='add_project'
    ),

    # ==========================================
    # CERTIFICATIONS
    # ==========================================

    path(
        'add-certification/',
        views.add_certification,
        name='add_certification'
    ),

    # ---------------------user profile ------------------
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # SKILLS
    path('skills/', views.skills_view, name='skills'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),

    # EDUCATION
    path('education/', views.education_view, name='education'),
    path('education/add/', views.add_education, name='add_education'),
    path('education/delete/<int:edu_id>/', views.delete_education, name='delete_education'),

    # EXPERIENCE
    path('experience/', views.experience_view, name='experience'),
path('experience/add/', views.add_experience, name='add_experience'),
path('experience/delete/<int:exp_id>/', views.delete_experience, name='delete_experience'),

    # PROJECTS
    path('projects/', views.projects_view, name='projects'),
path('projects/add/', views.add_project, name='add_project'),
path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),

# CERTIFICATIONS
path('certifications/', views.certifications_view, name='certifications'),
path('certifications/add/', views.add_certification, name='add_certification'),
path('certifications/delete/<int:cert_id>/', views.delete_certification, name='delete_certification'),

# resume
path('resume/', views.resume_view, name='resume'),

]