from . import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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
