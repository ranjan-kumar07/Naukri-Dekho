from django import forms
from django.contrib.auth.models import User

from .models import (
    Profile,
    Skill,
    Education,
    Experience,
    Project,
    Certification
)


# ==========================================
# REGISTER FORM
# ==========================================

class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),

        }


# ==========================================
# PROFILE FORM
# ==========================================

class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            'profile_image',
            'phone',
            'location',
            'date_of_birth',
            'gender',
            'bio',
            'resume',
            'linkedin',
            'github',
            'portfolio',
        ]

        widgets = {

            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location'
            }),

            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),

            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write something about yourself',
                'rows': 4
            }),

            'resume': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn Profile URL'
            }),

            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'GitHub Profile URL'
            }),

            'portfolio': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Portfolio Website URL'
            }),

        }


# ==========================================
# SKILL FORM
# ==========================================

class SkillForm(forms.ModelForm):

    class Meta:

        model = Skill

        fields = ['name']

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Skill'
            }),

        }


# ==========================================
# EDUCATION FORM
# ==========================================

class EducationForm(forms.ModelForm):

    class Meta:

        model = Education

        fields = [
            'college_name',
            'degree',
            'field_of_study',
            'start_year',
            'end_year'
        ]

        widgets = {

            'college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'College Name'
            }),

            'degree': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Degree'
            }),

            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Field Of Study'
            }),

            'start_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Start Year'
            }),

            'end_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'End Year'
            }),

        }


# ==========================================
# EXPERIENCE FORM
# ==========================================

class ExperienceForm(forms.ModelForm):

    class Meta:

        model = Experience

        fields = [
            'company_name',
            'job_role',
            'start_date',
            'end_date',
            'currently_working',
            'description'
        ]

        widgets = {

            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),

            'job_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Role'
            }),

            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'currently_working': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your work experience',
                'rows': 4
            }),

        }


# ==========================================
# PROJECT FORM
# ==========================================

class ProjectForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = [
            'title',
            'technologies_used',
            'github_link',
            'live_link',
            'description'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Title'
            }),

            'technologies_used': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python, Django, Bootstrap'
            }),

            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'GitHub Repository URL'
            }),

            'live_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Live Project URL'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Project Description',
                'rows': 4
            }),

        }


# ==========================================
# CERTIFICATION FORM
# ==========================================

class CertificationForm(forms.ModelForm):

    class Meta:

        model = Certification

        fields = [
            'title',
            'organization',
            'issue_date',
            'credential_url'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certificate Title'
            }),

            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization Name'
            }),

            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'credential_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Credential URL'
            }),

        }