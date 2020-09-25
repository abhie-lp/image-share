from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("images/", include("images.urls", namespace="images")),
    path('admin/', admin.site.urls),
    path("account/", include("account.urls")),
    path("", RedirectView.as_view(url="/account/", permanent=True))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
