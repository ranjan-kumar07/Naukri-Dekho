from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import RegisterForm
from jobs.models import Application
from jobs.models import Application


# ================= REGISTER =================

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            
            
            # Check username already exists
            username_exists = User.objects.filter(username=username).exists()

            # Check email already exists
            email_exists = User.objects.filter(email=email).exists()

            if username_exists and email_exists:
                messages.error(request, 'Username and Email already exist')
                return redirect('register')

            elif username_exists:
                messages.error(request, 'Username already exists')
                return redirect('register')

            elif email_exists:
                messages.error(request, 'Email already exists')
                return redirect('register')

            # Create user
            user = User.objects.create_user(

                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']

            )

            # Create profile
            Profile.objects.create(
                user=user,
                role=role
            )

            messages.success(request, 'Account created successfully')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# ================= LOGIN =================

def login_view(request):

    if request.user.is_authenticated:

        profile = Profile.objects.filter(user=request.user).first()

        if profile.role == 'user':
            return redirect('user_dashboard')

        elif profile.role == 'recruiter':
            return redirect('recruiter_dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            profile = Profile.objects.filter(user=user).first()

            if profile and profile.role == 'user':
                return redirect('user_dashboard')

            elif profile and profile.role == 'recruiter':
                return redirect('recruiter_dashboard')

        else:
            messages.error(request, 'Invalid Username or Password')

    return render(request, 'login.html')


# ================= USER DASHBOARD =================

@login_required(login_url='login')
def user_dashboard(request):

    applications = Application.objects.filter(
        user=request.user
    )

    pending_count = applications.filter(
        status='pending'
    ).count()

    interview_count = applications.filter(
        status='accepted'
    ).count()

    context = {

        'applications': applications,

        'pending_count': pending_count,

        'interview_count': interview_count,

    }

    return render(
        request,
        'user/user_dashboard.html',
        context
    )


# ================= RECRUITER DASHBOARD =================

@login_required(login_url='login')
def recruiter_dashboard(request):

    return render(request, 'recruiter/recruiter_dashboard.html')


# ================= LOGOUT =================

def logout_view(request):

    logout(request)
    messages.success(request, 'Logged out successfully')

    return redirect('home')