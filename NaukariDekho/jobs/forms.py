from django import forms
from .models import Job, Application
from datetime import date


# Apply Job Form
class ApplicationForm(forms.ModelForm):

    class Meta:

        model = Application

        fields = [
            'resume',
            'cover_letter'
        ]

        widgets = {

            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your cover letter...',
                'rows': 5
            }),
        }


# Add Job Form
class JobForm(forms.ModelForm):

    # Make application deadline required
    def __init__(self, *args, **kwargs):

        super(JobForm, self).__init__(*args, **kwargs)

        self.fields['application_deadline'].required = True

    class Meta:

        model = Job

        fields = [
            'title',
            'role',
            'company',
            'company_logo',
            'location',
            'salary_lpa',
            'description',
            'skills_required',
            'experience_required',
            'education_required',
            'job_type',
            'vacancies',
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

            'company_logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Bangalore'
            }),

            'salary_lpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 6.5'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write complete job description...',
                'rows': 5
            }),

            'skills_required': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Python, Django, SQL',
                'rows': 3
            }),

            'experience_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 2 Years'
            }),

            'education_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: B.Tech, MCA'
            }),

            'job_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'vacancies': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 5'
            }),

            # Calendar logic
            'application_deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': date.today().isoformat()
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
    def clean_salary_lpa(self):

        salary_lpa = self.cleaned_data.get('salary_lpa')

        if salary_lpa is not None:

            if salary_lpa <= 0:

                raise forms.ValidationError(
                    'Salary must be greater than 0.'
                )

            if salary_lpa < 1:

                raise forms.ValidationError(
                    'Salary looks too low.'
                )

        return salary_lpa

    # Description Validation
    def clean_description(self):

        description = self.cleaned_data.get('description')

        if description and len(description) < 20:

            raise forms.ValidationError(
                'Description must be at least 20 characters long.'
            )

        return description

    # Vacancies Validation
    def clean_vacancies(self):

        vacancies = self.cleaned_data.get('vacancies')

        if vacancies <= 0:

            raise forms.ValidationError(
                'Vacancies must be at least 1.'
            )

        return vacancies

    # Deadline Validation
    def clean_application_deadline(self):

        deadline = self.cleaned_data.get(
            'application_deadline'
        )

        # If no date selected
        if not deadline:

            return deadline

        # Prevent past dates
        if deadline < date.today():

            raise forms.ValidationError(
                'Deadline cannot be in the past.'
            )

        return deadline