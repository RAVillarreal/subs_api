import os
import shutil
import json
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import Http404, HttpResponse
from django.conf import settings
from .models import Subtitle
from .serializers import SubtitleSerializer
from .subtitles import get_from_subdivx, download, get_video_info


# Create your views here.
class SubtitleList(views.APIView):

    def get(self, request):

        # Obtener informacion de los videos
        files = json.loads(self.request.query_params["files"])
        files_info = get_video_info(files)
        video_name = files_info[0]["name"] + ' ' + files_info[0]["season"]
        folder_path = os.path.join(settings.MEDIA_ROOT, video_name)
        for file in files:
            try:
                subtitle = Subtitle.objects.get(name=file)
                link = subtitle.link
            except Subtitle.DoesNotExist:
                # Buscar en subdivx
                link = get_from_subdivx(file)

                if link:
                    # Guardar en BD
                    Subtitle.objects.create(name=file, link=link)
                else:
                    # Aqui deberia mandar un beta de que no se encontro
                    print("Subtitlo para %s no encontrado" % file)
                    continue

            # Descargar en carpeta
            download(file, link, folder_path)

        # Comprimir
        shutil.make_archive(video_name, 'zip', folder_path)

        # Retornar link de carpeta comprimida en JSON
        file_pointer = open(folder_path, "r")
        data = {
            "filename": video_name,
            "season": files_info[0].season,
            "link": file_pointer
        }
        return Response(data=data, status=status.HTTP_200_OK)
