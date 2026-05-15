from django import forms
from .models import Job, Application
from datetime import date

# To apply for job
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'resume',
            'cover_letter'
        ]

# Add job form
class JobForm(forms.ModelForm):

    # 1. Add the __init__ method to dynamically make fields required
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['application_deadline'].required = True
        
    class Meta:
        model = Job
        fields = [
            'title',
            'role',
            'company',
            'location',
            'salary',
            'description',
            'application_deadline'
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

            'application_deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
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
        if title and len(title) < 3:
            raise forms.ValidationError(
                'Job title must contain at least 3 characters.'
            )
        return title

    # Salary Validation
    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None:
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
        if description and len(description) < 20:
            raise forms.ValidationError(
                'Description must be at least 20 characters long.'
            )
        return description
    
    # Deadline Validation (Fixed Crash)
    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')

        # If the input is empty or unparseable, return it safely.
        # This allows Django's standard validation mechanics to handle the missing value.
        if not deadline:
            return deadline

        # It is now safe to compare because deadline is guaranteed to be a valid date object
        if deadline < date.today():
            raise forms.ValidationError(
                'Deadline cannot be in the past.'
            )

        return deadline