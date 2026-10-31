from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):

    class Role(models.TextChoices):
        MENTOR = "MENTOR", "Mentor"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

    def __str__(self):
        return self.username