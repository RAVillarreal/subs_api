from rest_framework import serializers
from .models import Subtitle

class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ("name", "link", "downloads", "date")