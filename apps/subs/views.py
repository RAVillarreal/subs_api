from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subs import Subtitle


class SubtitleView(APIView):

    def get_subtitle(self, name):
        try:
            subtitle = Subtitle.objects.get(name=name)
        except Subtitle.DoesNotExist:
            raise Http404

        return subtitle

    def get(self, request):
        name = self.request.query_params['name']
        if name:
            subtitle = self.get_subtitle(name)

        return Response(,status=status.HTTP_200_OK)