import os
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
            download_folder = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4()) + '/')
            for file in files:
                try:
                    subtitle = Subtitle.objects.get(name=file)
                    link = subtitle.link
                except Subtitle.DoesNotExist:
                    link = subtitles.get_from_subdivx(file)
                    if link:
                        Subtitle.objects.create(name=file, link=link)
                    else:
                        print("Subtitle for {0} not found.".format(file))
                        continue

                subtitles.download(file, link, download_folder)
            zip = subtitles.get_zip_file(download_folder)
            if zip:
                data = {
                    "video_information": subtitles.get_video_info(files[0]),
                    "files": len(zip.filelist),
                    "link": "http://localhost:8000/media/{0}".format(zip.filename.replace(settings.MEDIA_ROOT, '')),
                }
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)
              
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)