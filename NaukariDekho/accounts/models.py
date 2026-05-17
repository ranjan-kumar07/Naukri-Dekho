from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('recruiter', 'Recruiter'),
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

    bio = models.TextField(
        blank=True
    )

    skills = models.CharField(
        max_length=300,
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):

        return self.user.username
    
    