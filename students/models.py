from django.db import models
from accounts.models import Account

class Student(models.Model):
    #related_name is how this student column is stored in User Model
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='student_profile') 
    roll_number = models.CharField(max_length=20, unique=True) 
    phone = models.CharField(max_length=15) 
    address = models.TextField()
    #blank=True means optional, null=True allows database to store Null if no value given
    profile_picture = models.ImageField(upload_to='students/profiles', blank=True, null=True) 
    date_of_birth = models.DateField(blank=True, null=True) 

    def __str__(self):
        return f'{self.account.get_full_name()} ({self.roll_number})' 
    
    class Meta:
        permissions = [
            ('view_student_dashboard', 'Can view student dashboard'),
            ("view_student_list", "Can view student list"),
    ]