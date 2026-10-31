from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'is_active'   
    )
    list_filter = (
        'role', 
        'is_active', #shows whether a user account is active. True - can log in else cannot log in
        'is_staff'   #'is_staff' indicates whether the user can access the Django Admin (/admin)
    )
    fieldsets = UserAdmin.fieldsets + (
        ( 'Account Role', { 'fields' : ('role',) }),
    )
'''
fieldsets controls how fields are grouped on the Add/Edit User page in the Django Admin.
-The default UserAdmin already has sections like: Username & Password, Personal info, Permissions etc. 
-if you use + another section is added with name and fields
'''
