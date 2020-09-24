import redis

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from common.decorators import ajax_required

from actions.utils import create_action
from .forms import ImageCreateForm
from .models import Image

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@login_required
def image_ranking(request):
    # Get image ranking dictionary
    image_rankings = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    image_ranking_ids = tuple(int(_id) for _id in image_rankings)
    
    # Get the most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, "image/ranking.html",
                  {"section": "ranking", "most_viewed": most_viewed})


@login_required
def image_list(request, sort=None):
    images = Image.objects.all()
    following_ids = list(request.user.following.values_list("id", flat=True))
    if following_ids:
        images = images.filter(user__in=following_ids + [request.user.id])
    if sort:
        if sort == "popularity":
            images = images.order_by("-total_likes")
        elif sort == "recent":
            images = images.order_by("-created")
        else:
            return HttpResponseBadRequest()
    paginator = Paginator(images, 10)
    page = request.GET.get("page")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, "image/list_ajax.html",
                      {"section": "images", "images": images})
    return render(request, "image/list.html",
                  {"section": "images", "images": images})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, "bookmarked image", new_item)
            messages.success(request, "Image added successfully.")
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    
    return render(request, "image/create.html",
                  {"section": "images", "form": form})


def image_detail(request, pk, slug):
    image = get_object_or_404(Image, id=pk, slug=slug)
    total_views = r.incr(f"image:{image.id}:views")
    r.zincrby("image_ranking", 1, image.id)
    return render(request, "image/detail.html",
                  {"section": "images", "image": image,
                   "total_views": total_views})
