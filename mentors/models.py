from django.db import models
from accounts.models import Account


class Mentor(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='mentor_profile') 
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")

    def __str__(self):
        return self.account.get_full_name()
    class Meta:
        permissions = [
            ('view_mentor_dashboard', 'Can view mentor dashboard'),
            ("view_mentor_list", "Can view mentor list"),
    ]
        