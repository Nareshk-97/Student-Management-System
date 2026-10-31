from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import permission_required 
from students.models import Student 
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db import transaction
from accounts.forms import AccountCreateForm, AccountUpdateForm
from accounts.models import Account
from .forms import MentorForm
from .models import Mentor



# Create your views here.
@permission_required("accounts.add_account", raise_exception=True)
@permission_required("mentors.add_mentor", raise_exception=True)
@transaction.atomic
def mentor_create(request):
    if request.method == "POST":
        account_form = AccountCreateForm(request.POST)
        mentor_form = MentorForm(request.POST)
        if account_form.is_valid() and mentor_form.is_valid():
            # Create Account
            account = account_form.save(commit=False)
            account.role = Account.Role.MENTOR
            account.save()
            # Create Mentor profile
            mentor = mentor_form.save(commit=False)
            mentor.account = account
            mentor.save()
            # Add Group
            mentors_group = Group.objects.get(name="Mentors")
            account.groups.add(mentors_group)
            messages.success(request, "Mentor created successfully.")
            return redirect("mentor_list")
    else:
        account_form = AccountCreateForm()
        mentor_form = MentorForm()
    context = {
        "account_form": account_form,
        "mentor_form": mentor_form,
        "title": "Create Mentor",
    }
    return render(request, "mentors/mentor_form.html", context)



@permission_required("accounts.change_account", raise_exception=True)
@permission_required("mentors.change_mentor", raise_exception=True)
@transaction.atomic
def mentor_update(request, pk):
    mentor = get_object_or_404(Mentor.objects.select_related("account"),pk=pk,)
    if request.method == "POST":
        account_form = AccountUpdateForm(request.POST, instance=mentor.account,)
        mentor_form = MentorForm(request.POST, instance=mentor,)
        if account_form.is_valid() and mentor_form.is_valid():
            account_form.save()
            mentor_form.save()
            messages.success(request, "Mentor updated successfully.")
            return redirect("mentor_list")
    else:
        account_form = AccountUpdateForm(instance=mentor.account)
        mentor_form = MentorForm(instance=mentor)
    context = {
        "account_form": account_form,
        "mentor_form": mentor_form,
        "title": "Update Mentor",
    }
    return render(request, "mentors/mentor_form.html", context)


@permission_required("accounts.delete_account", raise_exception=True)
@permission_required("mentors.delete_mentor", raise_exception=True)
@transaction.atomic
def mentor_delete(request, pk):
    mentor = get_object_or_404(Mentor.objects.select_related("account"),pk=pk,)
    if request.method == "POST":
        mentor.account.delete()
        messages.success(request, "Mentor deleted successfully.")
        return redirect("mentor_list")

    return render(request,"mentors/mentor_confirm_delete.html",{"mentor": mentor,},)


@permission_required("mentors.view_mentor", raise_exception=True)
def mentor_detail(request, pk):
    mentor = get_object_or_404(
        Mentor.objects.select_related("account"),
        pk=pk,
    )
    return render(request,"mentors/mentor_detail.html",{"mentor": mentor,},)



@permission_required('mentors.view_mentor_dashboard', raise_exception=True)
def mentor_dashboard(request):
    #select_related is like join, to get details in account table
    students = Student.objects.select_related('account') 
    search = request.GET.get('search','').strip() 
    if search:
        students = students.filter(
            Q(account__username__icontains= search) | 
            Q(account__first_name__icontains = search) |
            Q(account__last_name__icontains = search) |
            Q(roll_number__icontains = search)
        )

    #divide
    paginator = Paginator(students,2) 
    #ask page number
    page_number = request.GET.get('page',1) #page numbering in Django starts from 1
    #age page
    page_obj = paginator.get_page(page_number)

    mentor = request.user.mentor_profile

    context = {
        "mentor": mentor,
        "page_obj": page_obj,
        "search": search,
    }

    return render(request, 'mentors/mentor_dashboard.html', context)



@permission_required("mentors.view_mentor_list", raise_exception=True)
def mentor_list(request):
    mentors = Mentor.objects.select_related("account")

    search = request.GET.get("search", "").strip()

    if search:
        mentors = mentors.filter(
            Q(account__username__icontains=search)
            | Q(account__first_name__icontains=search)
            | Q(account__last_name__icontains=search)
            | Q(department__icontains=search)
            | Q(qualification__icontains=search)
        )

    paginator = Paginator(mentors, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
            "page_obj": page_obj,
            "search": search,
    }

    return render(request, "mentors/mentor_list.html", context)