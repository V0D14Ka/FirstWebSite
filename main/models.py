from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    photo = models.ImageField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
