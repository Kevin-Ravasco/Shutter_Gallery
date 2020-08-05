from django.contrib import admin
from .models import Album, Photo, Profile


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'created_by',)
    search_fields = ['name']


class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", 'date_created', 'album']


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["first_name", 'last_name', 'phone']
    list_display = ["first_name", 'last_name', 'phone']


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, ImageAdmin)
admin.site.register(Profile, ProfileAdmin)
