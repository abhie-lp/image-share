from django.db import models
from django.conf import settings


def save_dp(instance, filename):
    username = instance.user.username
    extension = filename.rsplit(".", 1)[1]
    filename = username + "." + extension
    return "/".join([username[0], filename])


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to=save_dp, blank=True)

    def __str__(self):
        return self.user.username
