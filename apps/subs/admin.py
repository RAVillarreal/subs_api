from django.contrib import admin

from apps.subs.models import Subtitle


class SubtitleAdmin(admin.ModelAdmin):
    fields = ('name', 'link', 'downloads')


admin.site.register(Subtitle, SubtitleAdmin)
