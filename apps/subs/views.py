from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subs.models import Subtitle


class SubtitleView(APIView):

    @staticmethod
    def get_subtitle(name):
        try:
            subtitle = Subtitle.objects.get(name=name)
        except Subtitle.DoesNotExist:
            raise Http404

        return subtitle

    def get(self, request):
        name = request.query_params['name']
        if name:
            subtitle = self.get_subtitle(name)
            return Response(subtitle, status=status.HTTP_200_OK)

        return Response('Subtitle not found!', status=status.HTTP_404_NOT_FOUND)
