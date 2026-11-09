from django.db import models
from django.contrib.auth.models import User


# ==========================================
# PROFILE MODEL
# ==========================================
class Profile(models.Model):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('recruiter', 'Recruiter'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    profile_image = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    linkedin = models.URLField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    portfolio = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.user.username


# ==========================================
# SKILL MODEL
# ==========================================

class Skill(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='skills'
    )

    name = models.CharField(
        max_length=100
    )

    def __str__(self):

        return self.name


# ==========================================
# EDUCATION MODEL
# ==========================================

class Education(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='educations'
    )

    college_name = models.CharField(
        max_length=255
    )

    degree = models.CharField(
        max_length=255
    )

    field_of_study = models.CharField(
        max_length=255
    )

    start_year = models.IntegerField()

    end_year = models.IntegerField()

    def __str__(self):

        return f"{self.degree} - {self.college_name}"


# ==========================================
# EXPERIENCE MODEL
# ==========================================

class Experience(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='experiences'
    )

    company_name = models.CharField(
        max_length=255
    )

    job_role = models.CharField(
        max_length=255
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    currently_working = models.BooleanField(
        default=False
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):

        return self.company_name


# ==========================================
# PROJECT MODEL
# ==========================================

class Project(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    title = models.CharField(
        max_length=255
    )

    technologies_used = models.CharField(
        max_length=300
    )

    github_link = models.URLField(
        blank=True
    )

    live_link = models.URLField(
        blank=True
    )

    description = models.TextField()

    def __str__(self):

        return self.title


# ==========================================
# CERTIFICATION MODEL
# ==========================================

class Certification(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='certifications'
    )

    title = models.CharField(
        max_length=255
    )

    organization = models.CharField(
        max_length=255
    )

    issue_date = models.DateField()

    credential_url = models.URLField(
        blank=True
    )

    def __str__(self):

        return self.title