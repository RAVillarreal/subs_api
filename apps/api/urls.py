
from django.urls import path

from apps.subs.views import SubtitleView

app_name = 'api'

urlpatterns = [
    path('subtitles/', SubtitleView.as_view(), name='subtitle'),
]