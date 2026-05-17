from django import forms
from django.contrib.auth.models import User

from .models import Profile


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
            'class': 'form-control'
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
                'placeholder': 'Email'
            }),

        }


class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            'profile_image',
            'phone',
            'bio',
            'skills',
            'linkedin',
            'resume'
        ]

        widgets = {

            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write About Yourself',
                'rows': 4
            }),

            'skills': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python, Django, Java'
            }),

            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn Profile URL'
            }),

            'resume': forms.FileInput(attrs={
                'class': 'form-control'
            }),

        }