from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from actions.utils import create_action
from actions.models import Action
from common.decorators import ajax_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    print("user id", user_id)
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(
                    user_from=request.user, user_to=user
                )
                create_action(request.user, "is following", user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user
                ).delete()
            return JsonResponse({"status":  "ok"})
        except User.DoesNotExist:
            print("Error in except")
            return JsonResponse({"status": "error"})
    print("Error if bahar")
    return JsonResponse({"status": "error"})


@login_required
def users_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, "user/list.html",
                  {"section": "people", "users": users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, "user/detail.html", {"user": user})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "Error updating your profile.")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, "account/edit.html", {"user_form": user_form,
                                                 "profile_form": profile_form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user, "has created an account")
            messages.success(request, "Successfully created your new account.")
            return render(
                request, "account/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat=True)
    
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related("user", "user__profile")\
                     .prefetch_related("target")[:10]
    print(actions)
    return render(request, "account/dashboard.html",
                  {"section": "dashboard", "actions": actions})
