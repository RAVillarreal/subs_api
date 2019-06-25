import os
import shutil
import uuid
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from apps.subs.models import Subtitle
from apps.subs.subtitles import get_video_info, get_from_subdivx, download


class SubtitlesView(APIView):

    def post(self, request):

        # Obtain video information
        files = request.POST.get('files')
        files_info = get_video_info(files)

        if files:

            download_path = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4()))

            if not os.path.exists(download_path):
                os.makedirs(download_path)

            for file in files:
                subtitle, created = Subtitle.objects.get_or_create(
                    name=file,
                    defaults={"link": get_from_subdivx(file)}
                )

                # Descargar en carpeta
                download(subtitle.name, subtitle.link, download_path)

            # Comprobar archivos descargados es serie o pelicula

            if "season" in files_info[0]:
                file_name = (files_info[0]["title"] + ' ' + str(files_info[0]["season"])).replace(' ', '.')
                new_download_path = os.path.join(settings.MEDIA_ROOT, file_name)
                os.rename(download_path, new_download_path)
                data = {
                    "title": files_info[0]["title"],
                    "season": str(files_info[0]["season"]),
                    "episodes": str(len(files)),
                    "link": r'http://localhost:8000/media/' + file_name + '.zip'
                }
            else:
                file_name = (files_info[0]["title"]).replace(' ', '.')
                new_download_path = os.path.join(settings.MEDIA_ROOT, file_name)
                os.rename(download_path, new_download_path)
                data = {
                    "filename": files_info[0]["title"],
                    "link": r'http://localhost:8000/media/' + file_name + '.zip',
                }

            # Comprimir
            shutil.make_archive(new_download_path, 'zip', new_download_path)
            shutil.rmtree(new_download_path)

            return Response(data=data, status=status.HTTP_200_OK)

        else:
            return Response(data='Bad Request', status=status.HTTP_400_BAD_REQUEST)
