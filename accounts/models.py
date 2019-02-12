from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def save_dp(instance, filename):
    username = instance.user.username
    extension = filename.rsplit(".", 1)[1]
    filename = username + "." + extension
    return "/".join([username[0], filename])


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=save_dp, blank=True)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user_from = models.ForeignKey("auth.User", related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey("auth.User", related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = "-created",
    
    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# Add 'following' field dynamically to User model
User.add_to_class("following",
                   models.ManyToManyField("self",
                                           through=Contact,
                                           related_name="followers",
                                           symmetrical=False))