from . import forms, models

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# def user_login(request):
#     if request.method == "POST":
#         form = forms.LoginForm(data=request.POST)

#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd["username"], password=cd["password"])

#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse("Authenticated successfully.")
#                 else:
#                     return HttpResponse("Disabled account.")
#             else:
#                 return HttpResponse("Invalid login.")
#     else:
#         form = forms.LoginForm()

#     return render(request, "accounts/login.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html", {"section": "dashboard"})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user_form = forms.UserRegistrationForm(data=request.POST)
        
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password for the user
            new_user.set_password(user_form.cleaned_data["password"])
            # Now save the user to the db
            new_user.save()
            models.Profile.objects.create(user=new_user)

            return render(request, "accounts/register_done.html", {"new_user": new_user})
    else:
        user_form = forms.UserRegistrationForm()
    
    return render(request, "accounts/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)
        profile_form = forms.ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )

        if user_form.is_valid() and profile_form:
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "Error updating your profile.")
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    
    return render(request, "accounts/edit.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, "accounts/user_list.html", {"section": "people", "users": users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, "accounts/user_detail.html", {"section": "people", "user": user})
