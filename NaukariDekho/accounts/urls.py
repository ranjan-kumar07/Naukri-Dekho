from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),

    path('logout/', views.logout_view, name='logout'),
    
    path(
    'profile/',
    views.profile,
    name='profile'
),

path(
    'update-profile-image/',
    views.update_profile_image,
    name='update_profile_image'
),
    
]