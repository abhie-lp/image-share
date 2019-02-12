from django.db import models
from django.conf import settings
from django.utils.text import slugify


def save_image(instance, filename):
    username = instance.user.username
    return "/".join(["uploads", username[0], username, filename])


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images_created")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    url = models.URLField()
    image = models.ImageField(upload_to=save_image)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="images_liked", blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # storage, path = self.image.storage, self.image.path
        # super(Image, self).delete(*args, **kwargs)
        # storage.delete(path)

        self.image.delete()
        super(Image, self).delete(*args, **kwargs)
