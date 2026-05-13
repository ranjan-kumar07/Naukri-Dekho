from django import forms
from .models import Job

from .models import Application

# To apply for job
class ApplicationForm(forms.ModelForm):

    class Meta:

        model = Application

        fields = [
            'resume',
            'cover_letter'
        ]

#  Add job form

class JobForm(forms.ModelForm):

    class Meta:

        model = Job

        fields = [
            'title',
            'role',
            'company',
            'location',
            'salary',
            'description'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Python Developer'
            }),

            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Infosys'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Bangalore'
            }),

            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 50000'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write complete job description...',
                'rows': 5
            }),

            'role': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[

                ('', 'Select Job Role'),

                ('Backend Developer', 'Backend Developer'),
                ('Frontend Developer', 'Frontend Developer'),
                ('Full Stack Developer', 'Full Stack Developer'),
                ('Data Analyst', 'Data Analyst'),
                ('UI/UX Designer', 'UI/UX Designer'),
                ('Mobile App Developer', 'Mobile App Developer'),
                ('Java Developer', 'Java Developer'),
                ('Python Developer', 'Python Developer'),
                ('DevOps Engineer', 'DevOps Engineer'),

            ]),

        }

    # Title Validation
    def clean_title(self):

        title = self.cleaned_data.get('title')

        if len(title) < 3:

            raise forms.ValidationError(
                'Job title must contain at least 3 characters.'
            )

        return title

    # Salary Validation
    def clean_salary(self):

        salary = self.cleaned_data.get('salary')

        if salary <= 0:

            raise forms.ValidationError(
                'Salary must be greater than 0.'
            )

        if salary < 5000:

            raise forms.ValidationError(
                'Salary looks too low.'
            )

        return salary

  

    # Description Validation
    def clean_description(self):

        description = self.cleaned_data.get('description')

        if len(description) < 20:

            raise forms.ValidationError(
                'Description must be at least 20 characters long.'
            )

        return description