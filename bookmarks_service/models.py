from django.contrib.auth.models import User
from django.db import models


class Bookmark(models.Model):
    favicon = models.CharField('Favicon', max_length=250, blank=True)
    title = models.CharField('Title', max_length=150, blank=True)
    url = models.URLField('URL', max_length=150)
    description = models.TextField('Description', blank=True)
    add_by_user = models.ManyToManyField(User)

    def __str__(self):
        return self.url
