import os

from django.db import models
from django.contrib.auth.models import User


from ShutterGallery import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='/profiles/default_user.png', upload_to='profiles')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Album(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_cover_photo(self):
        return Photo.objects.filter(album=self).first()

    def get_all_photos(self):
        return Photo.objects.filter(album=self)


class Photo(models.Model):
    image = models.ImageField()
    date_created = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album')

    def __unicode__(self):
        return self.image.name

