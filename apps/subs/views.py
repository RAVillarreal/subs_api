import os
import shutil
import json
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Subtitle
from apps.subs import subtitles


# Create your views here.
class SubtitlesView(APIView):

    def get(self, request):
    	""" Get subtitles from subdivx and return zip link """

      files = json.loads(self.request.query_params["files"])
      if files:
          for file in files:
              try:
                  subtitle = Subtitle.objects.get(name=file)
                  link = subtitle.link
              except Subtitle.DoesNotExist:
                  link = get_from_subdivx(file)
                  if link:
                      Subtitle.objects.create(name=file, link=link)
                  else:
                      print("Subtitle for {0} not found.".format(file))
                      continue
                      
              download(file, link, uuid4())

         	zip = subtitles.get_zip_file()
         	if zip:
         		data = {
         			"filename": zip.filename,
         			"files": zip.length,
         			"link": zip.link,
         		}
         		return Response(data=data, status=status.HTTP_200_OK)

         	return Respose(status=status.HTTP_404_NOT_FOUND)
          
      else:
          return Response(status=status.HTTP_400_BAD_REQUEST)