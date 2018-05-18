import requests
import re
import urllib
from rest_framework import views
from rest_framework.response import Response
from bs4 import BeautifulSoup

# Create your views here.
class SubtitleDetail(views.APIView):
