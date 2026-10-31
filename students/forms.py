from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("account",)
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

 