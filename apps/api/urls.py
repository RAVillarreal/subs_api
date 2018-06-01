from apps.subs.views import SubtitlesView
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('subtitles/', SubtitlesView.as_view(), name='subtitle-list'),
]