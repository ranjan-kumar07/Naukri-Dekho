from django import forms

from .models import Donation


class DonationForm(forms.ModelForm):

    class Meta:

        model = Donation

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'amount'
        ]

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Donation Amount'
            }),

        }