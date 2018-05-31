from .views import SubtitleList
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('subtitles/', SubtitleList.as_view(), name='subtitle-list'),
]