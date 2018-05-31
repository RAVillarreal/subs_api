from apps.subs.views import SubtitleView
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('subtitle/', SubtitleView.as_view(), name='subtitle-list'),
]