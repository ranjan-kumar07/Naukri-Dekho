from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from accounts.models import Profile
from jobs.models import Job, Application
from django.db.models import Q
from django.utils import timezone

# ==========================================
# ADMIN DASHBOARD
# ==========================================
@staff_member_required(login_url='login')
def dashboard(request):

    # USERS
    total_users = Profile.objects.count()
    recruiters = Profile.objects.filter(role='recruiter').count()
    normal_users = Profile.objects.filter(role='user').count()
    admins = User.objects.filter(is_staff=True, is_superuser=False).count()

    # JOBS
    total_jobs = Job.objects.count()

    # APPLICATIONS
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status='pending').count()
    accepted_applications = Application.objects.filter(status='accepted').count()

    context = {
        "total_users": total_users,
        "recruiters": recruiters,
        "normal_users": normal_users,
        "admins": admins,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "accepted_applications": accepted_applications,
    }

    return render(request, 'adminpanel/dashboard.html', context)


# ==========================================
# USERS MANAGEMENT (FULL CONTROL)
# ==========================================
@staff_member_required(login_url='login')
def users(request):

    profiles = Profile.objects.select_related('user').all().order_by('-id')

    return render(request, 'adminpanel/users.html', {
        'profiles': profiles
    })


# ==========================================
# CHANGE ROLE (user <-> recruiter)
# ==========================================
@staff_member_required(login_url='login')
def change_role(request, profile_id, role):

    profile = get_object_or_404(Profile, id=profile_id)

    if role in ['user', 'recruiter']:
        profile.role = role
        profile.save()

    return redirect('admin_users')


# ==========================================
# MAKE ADMIN
# ==========================================
@staff_member_required(login_url='login')
def make_admin(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if not user.is_superuser:
        user.is_staff = True
        user.save()

    return redirect('admin_users')


# ==========================================
# REMOVE ADMIN
# ==========================================
@staff_member_required(login_url='login')
def remove_admin(request, user_id):

    user = get_object_or_404(User, id=user_id)

    # prevent removing yourself accidentally
    if request.user.id != user.id and not user.is_superuser:
        user.is_staff = False
        user.save()

    return redirect('admin_users')


# ==========================================
# DELETE USER (SAFE)
# ==========================================
@staff_member_required(login_url='login')
def delete_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    # SAFETY: never delete superuser
    if not user.is_superuser:
        user.delete()

    return redirect('admin_users')

# ==========================================
#  USER filter
# ==========================================

@staff_member_required(login_url='login')
def users(request):

    profiles = Profile.objects.select_related('user').all().order_by('-id')

    # SEARCH
    query = request.GET.get('q')
    role_filter = request.GET.get('role')

    if query:
        profiles = profiles.filter(
            user__username__icontains=query
        ) | profiles.filter(
            user__email__icontains=query
        )

    # FILTER ROLE
    if role_filter:
        if role_filter == 'admin':
            profiles = profiles.filter(user__is_staff=True)
        else:
            profiles = profiles.filter(role=role_filter)

    return render(request, 'adminpanel/users.html', {
        'profiles': profiles,
        'query': query,
        'role_filter': role_filter
    })


# -------------RECRUITER
# ==========================================
# RECRUITER MANAGEMENT
# ==========================================


@staff_member_required(login_url='login')
def recruiters(request):

    query = request.GET.get('q', '')

    profiles = (

    Profile.objects
    .select_related('user')
    .filter(
        role='recruiter',
        user__is_staff=False,
        user__is_superuser=False
    )

)

    if query:

        profiles = profiles.filter(

            Q(user__username__icontains=query) |
            Q(user__email__icontains=query)

        )

    recruiter_data = []

    for profile in profiles:

        # FIXED HERE
        recruiter_jobs = Job.objects.filter(
            recruiter=profile.user
        )

        total_jobs = recruiter_jobs.count()

        total_applications = (

            Application.objects.filter(
                job__in=recruiter_jobs
            ).count()

        )

        accepted = (

            Application.objects.filter(
                job__in=recruiter_jobs,
                status='accepted'
            ).count()

        )

        recruiter_data.append({

            'profile': profile,

            'jobs': total_jobs,

            'applications': total_applications,

            'accepted': accepted,

            'active': profile.user.is_active,

            'admin': profile.user.is_staff

        })

    return render(

        request,

        'adminpanel/recruiters.html',

        {

            'recruiters': recruiter_data,

            'query': query

        }

    )


# ==========================================
# ADMIN JOB MANAGEMENT
# ==========================================

@staff_member_required(login_url='login')
def jobs(request):

    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    jobs = (

        Job.objects
        .select_related('recruiter')
        .all()
        .order_by('-id')

    )

    # SEARCH

    if query:

        jobs = jobs.filter(

            Q(title__icontains=query) |

            Q(company__icontains=query) |

            Q(location__icontains=query) |

            Q(recruiter__username__icontains=query)

        )

    today = timezone.now().date()

    # STATUS FILTER

    if status == 'active':

        jobs = jobs.filter(
            application_deadline__gte=today
        )

    elif status == 'expired':

        jobs = jobs.filter(
            application_deadline__lt=today
        )

    job_data = []

    for job in jobs:

        total_applications = (

            Application.objects.filter(
                job=job
            ).count()

        )

        expired = (

            job.application_deadline
            <
            today

        )

        job_data.append({

            'job': job,

            'applications': total_applications,

            'expired': expired

        })

    return render(

        request,

        'adminpanel/jobs.html',

        {

            'jobs': job_data,

            'query': query,

            'status': status

        }

    )
# ==========================================
# DELETE JOB
# ==========================================
@staff_member_required(login_url='login')
def delete_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)
    job.delete()

    return redirect('admin_jobs')


# ==========================================
# APPLICATION MANAGEMENT
# ==========================================

@staff_member_required(login_url='login')
def applications(request):

    query = request.GET.get('q', '')

    applications = (
        Application.objects
        .select_related(
            'user',
            'job'
        )
        .all()
        .order_by('-applied_at')
    )

    if query:

        applications = applications.filter(
            user__username__icontains=query
        ) | applications.filter(
            job__title__icontains=query
        )

    return render(

        request,

        'adminpanel/applications.html',

        {
            'applications': applications,
            'query': query
        }

    )


# CHANGE STATUS
@staff_member_required(login_url='login')
def change_application_status(
    request,
    application_id,
    status
):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    valid_status = [

        'applied',
        'reviewing',
        'shortlisted',
        'accepted',
        'rejected'

    ]

    if status in valid_status:

        application.status = status
        application.save()

    return redirect(
        'admin_applications'
    )


# DELETE APPLICATION
@staff_member_required(login_url='login')
def delete_application(
    request,
    application_id
):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    application.delete()

    return redirect(
        'admin_applications'
    )