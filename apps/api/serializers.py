from rest_framework import serializers

from apps.subs.models import Subtitle


class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ("name", "link", "downloads", "date")
