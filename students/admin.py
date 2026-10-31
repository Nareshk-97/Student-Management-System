from django.contrib import admin
from .models import Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'roll_number',
        'phone',
        'date_of_birth'
    )
    search_fields = (
        'account__username',  #username is in User model
    )