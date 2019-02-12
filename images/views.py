from . import forms, models
from actions.utils import create_action
from image_share.common.decorators import ajax_required

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

import redis

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


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
            create_action(request.user, "bookmarked image", new_item)
            messages.success(request, "Image added successfully.")

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data created item detail view
        form = forms.ImageCreateForm(data=request.GET)
    
    return render(request, "images/create.html", {"section": "images", "form": form})


def image_detail(request, id, slug):
    image = get_object_or_404(models.Image, id=id, slug=slug)
    # increment total image view by 1
    total_views = r.incr("image:{}:views".format(image.id))
    # inrement image ranking by 1
    r.zincrby("image_ranking", 1, image.id)
    return render(request, 'images/detail.html', {"section": "images",
                                                  "image": image,
                                                  "total_views": total_views})


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
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            
            return JsonResponse({"status": "ok"})
        except:
            pass
    
    return JsonResponse({"status": "ko"})


@login_required
def image_list(request):
    images = models.Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return empty page
            return HttpResponse("")
        
        # If page is out  of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    
    if request.is_ajax():
        return render(request, "images/image_list_ajax.html", {"section": "images", "images": images})
    
    return render(request, "images/image_list.html", {"section": "images", "images": images})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    print("image ranking", image_ranking)
    image_ranking_ids = [int(id) for id in image_ranking]

    # get most viewed images
    most_viewed = list(models.Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x:image_ranking_ids.index(x.id))

    print(most_viewed)

    return render(request, "images/ranking.html", {"section": "images", "most_viewed": most_viewed})
