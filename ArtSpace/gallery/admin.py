from django.contrib import admin
from .models import Category, Artwork, Comment

admin.site.register(Category)
admin.site.register(Artwork)
admin.site.register(Comment)
