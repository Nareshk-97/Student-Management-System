from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import Account 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class AccountCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )