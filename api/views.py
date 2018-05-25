import os
import shutil
import json
import uuid
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Subtitle
from .subtitles import get_from_subdivx, download, get_video_info


# Create your views here.
class SubtitleList(views.APIView):

    def get(self, request):

        # Obtener informacion de los videos
        files = json.loads(self.request.query_params["files"])
        files_info = get_video_info(files)

        # Hacer carpeta
        folder_path = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4()))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

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

        #Comprobar archivos descargados

        # Es serie o pelicula
        if "season" in files_info[0]:
            file_name = (files_info[0]["title"] + ' ' + str(files_info[0]["season"])).replace(' ', '.')
            new_folder_path = os.path.join(settings.MEDIA_ROOT, file_name)
            os.rename(folder_path, new_folder_path)
            data = {
                "title": files_info[0]["title"],
                "season": str(files_info[0]["season"]),
                "episodes": str(len(files)),
                "link": r'http://localhost:8000/media/' + file_name + '.zip'
            }
        else:
            file_name = (files_info[0]["title"]).replace(' ', '.')
            new_folder_path = os.path.join(settings.MEDIA_ROOT, file_name)
            os.rename(folder_path, new_folder_path)
            data = {
                "filename": files_info[0]["title"],
                "link": r'http://localhost:8000/media/' + file_name + '.zip',
            }

        # Comprimir
        shutil.make_archive(new_folder_path, 'zip', new_folder_path)
        shutil.rmtree(new_folder_path)

        # Retornar JSON
        return Response(data=data, status=status.HTTP_200_OK)