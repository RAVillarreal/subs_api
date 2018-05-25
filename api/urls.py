from .views import *
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('subtitle/', SubtitleList.as_view(), name='subtitle-list'),
]