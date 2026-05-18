from django.db import models
from django.contrib.auth.models import User

# Job Model
class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )

    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    role = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    company_logo = models.ImageField(
        upload_to='company_logos/',
        null=True,
        blank=True
    )

    location = models.CharField(max_length=200)

    salary_lpa = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    description = models.TextField()

    skills_required = models.TextField(
        help_text="Example: Python, Django, SQL"
    )

    experience_required = models.CharField(
        max_length=100
    )

    education_required = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES
    )

    vacancies = models.IntegerField(default=1)

    application_deadline = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.title} at {self.company}"


# Application Model

class Application(models.Model):

    STATUS_CHOICES = (

        ('applied', 'Applied'),

        ('reviewing', 'Reviewing'),

        ('shortlisted', 'Shortlisted'),

        ('accepted', 'Accepted'),

        ('rejected', 'Rejected'),

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    resume = models.FileField(
        upload_to='resumes/'
    )

    cover_letter = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )

    recruiter_message = models.TextField(
        null=True,
        blank=True
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = ('user', 'job')

    def __str__(self):

        return f"{self.user.username} applied for {self.job.title}"