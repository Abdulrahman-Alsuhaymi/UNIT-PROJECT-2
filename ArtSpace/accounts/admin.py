from django.contrib import admin
from .models import ArtistProfile

# Register your models here.
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_pic')
    list_filter = ('user__is_active',)
    search_fields = ('user__username', 'user__email', 'bio')

admin.site.register(ArtistProfile, ArtistProfileAdmin)
