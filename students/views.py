from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.db import transaction
from accounts.forms import AccountCreateForm, AccountUpdateForm
from accounts.models import Account
from .models import Student
from .forms import StudentForm
from django.core.paginator import Paginator
from django.db.models import Q

@permission_required("accounts.add_account", raise_exception=True)
@permission_required("students.add_student", raise_exception=True)
@transaction.atomic
def student_create(request):
    if request.method == "POST":
        account_form = AccountCreateForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES,)
        if account_form.is_valid() and student_form.is_valid():
            try:
                account = account_form.save(commit=False)
                account.role = Account.Role.STUDENT
                account.save()

                student = student_form.save(commit=False)
                student.account = account
                student.save()

                students_group = Group.objects.get(name="Students")
                account.groups.add(students_group)

                messages.success(request, "Student created successfully.")
                return redirect("student_list")

            except Exception as e:
                print("ERROR:", repr(e))
                raise
    else:
        account_form = AccountCreateForm()
        student_form = StudentForm()
    context = {
        "account_form": account_form,
        "student_form": student_form,
        "title": "Create Student"
    }
    return render(request, "students/student_form.html", context)



@permission_required("accounts.change_account", raise_exception=True)
@permission_required("students.change_student", raise_exception=True)
@transaction.atomic
def student_update(request, pk):
    student = get_object_or_404(Student.objects.select_related("account"),pk=pk,)
    if request.method == "POST":
        account_form = AccountUpdateForm(request.POST, instance=student.account,)
        student_form = StudentForm(request.POST,request.FILES,instance=student,)
        if account_form.is_valid() and student_form.is_valid():
            account_form.save()
            student_form.save()
            messages.success(request,"Student updated successfully.")
            return redirect("student_list")
    else:
        account_form = AccountUpdateForm(instance=student.account)
        student_form = StudentForm(instance=student)
    context = {
        "account_form": account_form,
        "student_form": student_form,
        "title": "Update Student",
    }
    return render(request, "students/student_form.html", context)


@permission_required("accounts.delete_account", raise_exception=True)
@permission_required("students.delete_student", raise_exception=True)
@transaction.atomic
def student_delete(request, pk):
    student = get_object_or_404(Student.objects.select_related("account"), pk=pk,)

    if request.method == "POST":
        # deleting account deletes student because of OneToOne CASCADE
        student.account.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html",{"student": student,},)


@permission_required("students.view_student", raise_exception=True)
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related("account"), pk=pk,)
    return render(request, "students/student_detail.html", { "student": student,},)


@permission_required("students.view_student_dashboard", raise_exception=True,)
def student_dashboard(request):
    student = request.user.student_profile
    return render(request, "students/student_dashboard.html", {"student": student,},)

@permission_required("students.view_student_list", raise_exception=True)
def student_list(request):
    students = Student.objects.select_related("account")

    search = request.GET.get("search", "").strip()

    if search:
        students = students.filter(
            Q(account__username__icontains=search)
            | Q(account__first_name__icontains=search)
            | Q(account__last_name__icontains=search)
            | Q(roll_number__icontains=search)
        )

    paginator = Paginator(students, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(request, "students/student_list.html", context)