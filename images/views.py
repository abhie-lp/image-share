from . import forms, models
from image_share.common.decorators import ajax_required

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
def image_create(request):
    if request.method == "POST":
        #  If form is sent
        form = forms.ImageCreateForm(data=request.POST)

        if form.is_valid():
            # Form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False, user=request.user)
            # Assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image added successfully.")

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data created item detail view
        form = forms.ImageCreateForm(data=request.GET)
    
    return render(request, "images/create.html", {"section": "images", "form": form})


def image_detail(request, id, slug):
    image = get_object_or_404(models.Image, id=id, slug=slug)
    return render(request, 'images/detail.html', {"section": "images", "image": image})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = models.Image.objects.get(id=image_id)

            if action == "like":
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            
            return JsonResponse({"status": "ok"})
        except:
            pass
    
    return JsonResponse({"status": "ko"})
