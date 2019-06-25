from django.urls import path

from apps.api.views import SubtitlesView

app_name = 'api'

urlpatterns = [
    path('subtitles/', SubtitlesView.as_view()),
]
