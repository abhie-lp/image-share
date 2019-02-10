from . import forms, models

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required



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
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    
    return render(request, "accounts/edit.html", {"user_form": user_form, "profile_form": profile_form})
