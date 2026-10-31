from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Account


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role", Account.Role.STUDENT)
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([username, first_name, email, password, confirm_password]):
            messages.error(request, "Please fill in all required fields.")

        elif Account.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        elif Account.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif role not in [Account.Role.STUDENT, Account.Role.MENTOR]:
            messages.error(request, "Invalid role selected.")

        else:
            try:
                validate_password(password)
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
            else:
                Account.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    role=role,
                )

                messages.success(
                    request,
                    "Registration successful. Please log in."
                )
                return redirect("login")

    return render(request, "accounts/register.html")


@login_required
def login_success(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")

    elif request.user.role == Account.Role.MENTOR:
        return redirect("mentor_dashboard")

    elif request.user.role == Account.Role.STUDENT:
        return redirect("student_dashboard")

    else:
        return redirect("login")


@staff_member_required(login_url="login")
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")