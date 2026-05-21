from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Profile,
    Skill,
    Education,
    Experience,
    Project,
    Certification
)

from .forms import (
    RegisterForm,
    ProfileForm,
    SkillForm,
    EducationForm,
    ExperienceForm,
    ProjectForm,
    CertificationForm
)

from jobs.models import Application
from .utils import calculate_profile_completion


# ==========================================
# REGISTER
# ==========================================
def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('register')

            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=username,
                email=email,
                password=form.cleaned_data['password']
            )

            # SAFE PROFILE CREATION (FIXED)
            Profile.objects.create(user=user, role=role)

            messages.success(request, "Account created successfully")
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# ==========================================
# LOGIN
# ==========================================
def login_view(request):

    # If already logged in
    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect('/adminpanel/')

        profile = getattr(request.user, 'profile', None)

        if profile and profile.role == 'recruiter':
            return redirect('recruiter_dashboard')

        return redirect('user_dashboard')

    # LOGIN POST
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ADMIN FIRST
            if user.is_staff:
                return redirect('admin_dashboard')

            profile = getattr(user, 'profile', None)

            if profile and profile.role == 'recruiter':
                return redirect('recruiter_dashboard')

            return redirect('user_dashboard')

        messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')


# ==========================================
# LOGOUT
# ==========================================
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


# ==========================================
# USER DASHBOARD
# ==========================================
@login_required(login_url='login')
def user_dashboard(request):

    applications = Application.objects.filter(user=request.user)

    return render(request, 'user/user_dashboard.html', {
        'applications': applications,
        'pending_count': applications.filter(status='pending').count(),
        'interview_count': applications.filter(status='accepted').count(),
    })


# ==========================================
# RECRUITER DASHBOARD
# ==========================================
@login_required(login_url='login')
def recruiter_dashboard(request):
    return render(request, 'recruiter/recruiter_dashboard.html')


# ==========================================
# PROFILE VIEW
# ==========================================
@login_required(login_url='login')
def profile_view(request):

    profile = getattr(request.user, 'profile', None)

    completion = calculate_profile_completion(profile)

    return render(request, 'user/profile.html', {
        'profile': profile,
        'skills': profile.skills.all() if profile else [],
        'educations': profile.educations.all() if profile else [],
        'experiences': profile.experiences.all() if profile else [],
        'projects': profile.projects.all() if profile else [],
        'certifications': profile.certifications.all() if profile else [],
        'completion': completion,
        'active_page': 'overview'
    })


# ==========================================
# EDIT PROFILE
# ==========================================
@login_required
def edit_profile(request):

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', {
        'form': form,
        'active_page': 'edit_profile'
    })


# ==========================================
# SKILLS
# ==========================================
@login_required(login_url='login')
def skills_view(request):

    profile = request.user.profile
    skills = Skill.objects.filter(profile=profile)

    return render(request, 'user/skills.html', {
        'skills': skills,
        'active_page': 'skills'
    })


@login_required(login_url='login')
def add_skill(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = profile
            skill.save()
            return redirect('skills')

    else:
        form = SkillForm()

    return render(request, 'user/add_skill.html', {
        'form': form,
        'active_page': 'skills'
    })


@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, profile__user=request.user)
    skill.delete()
    return redirect('skills')


# ==========================================
# EDUCATION
# ==========================================
@login_required
def education_view(request):

    profile = request.user.profile
    educations = Education.objects.filter(profile=profile)

    return render(request, 'user/education.html', {
        'educations': educations,
        'active_page': 'education'
    })


@login_required
def add_education(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = EducationForm(request.POST)

        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = profile
            edu.save()
            return redirect('education')

    else:
        form = EducationForm()

    return render(request, 'user/add_education.html', {
        'form': form,
        'active_page': 'education'
    })


@login_required
def delete_education(request, edu_id):
    edu = get_object_or_404(Education, id=edu_id, profile__user=request.user)
    edu.delete()
    return redirect('education')


# ==========================================
# EXPERIENCE
# ==========================================
@login_required
def experience_view(request):

    profile = request.user.profile
    experiences = Experience.objects.filter(profile=profile)

    return render(request, 'user/experience.html', {
        'experiences': experiences,
        'active_page': 'experience'
    })


@login_required
def add_experience(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = ExperienceForm(request.POST)

        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = profile

            if exp.currently_working:
                exp.end_date = None

            exp.save()
            return redirect('experience')

    else:
        form = ExperienceForm()

    return render(request, 'user/add_experience.html', {
        'form': form,
        'active_page': 'experience'
    })


@login_required
def delete_experience(request, exp_id):
    exp = get_object_or_404(Experience, id=exp_id, profile__user=request.user)
    exp.delete()
    return redirect('experience')


# ==========================================
# PROJECTS
# ==========================================
@login_required
def projects_view(request):

    profile = request.user.profile
    projects = Project.objects.filter(profile=profile)

    return render(request, 'user/projects.html', {
        'projects': projects,
        'active_page': 'projects'
    })


@login_required
def add_project(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            return redirect('projects')

    else:
        form = ProjectForm()

    return render(request, 'user/add_project.html', {
        'form': form,
        'active_page': 'projects'
    })


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, profile__user=request.user)
    project.delete()
    return redirect('projects')


# ==========================================
# CERTIFICATIONS
# ==========================================
@login_required
def certifications_view(request):

    profile = request.user.profile
    certifications = Certification.objects.filter(profile=profile)

    return render(request, 'user/certifications.html', {
        'certifications': certifications,
        'active_page': 'certifications'
    })


@login_required
def add_certification(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = CertificationForm(request.POST)

        if form.is_valid():
            cert = form.save(commit=False)
            cert.profile = profile
            cert.save()
            return redirect('certifications')

    else:
        form = CertificationForm()

    return render(request, 'user/add_certification.html', {
        'form': form,
        'active_page': 'certifications'
    })


@login_required
def delete_certification(request, cert_id):
    cert = get_object_or_404(Certification, id=cert_id, profile__user=request.user)
    cert.delete()
    return redirect('certifications')


# ==========================================
# RESUME
# ==========================================
@login_required
def resume_view(request):

    profile = request.user.profile

    if request.method == 'POST':
        profile.linkedin = request.POST.get('linkedin')
        profile.github = request.POST.get('github')
        profile.portfolio = request.POST.get('portfolio')

        if request.FILES.get('resume'):
            profile.resume = request.FILES['resume']

        profile.save()
        return redirect('resume')

    return render(request, 'user/resume.html', {
        'profile': profile,
        'active_page': 'resume'
    })