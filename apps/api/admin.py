from django.contrib import admin
from .models import Subtitle

# Register your models here.
class SubtitleAdmin(admin.ModelAdmin):
    fields = ('name', 'link', 'downloads')

admin.site.register(Subtitle, SubtitleAdmin)