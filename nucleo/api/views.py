from django.views import View
from rest_framework import viewsets

from nucleo.api.serializers import TipoDocumentoSerializer
from nucleo.models.tipo_documento import TipoDocumento
from nucleo.models.usuario_abstract import GENERO
from django.http.response import JsonResponse


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer


class listarGenerosViewSet(View):
    def get(self, request):
        ls = []
        for item in GENERO:
            dict = {}
            dict['id'] = item[0]
            dict['nombre'] = item[1]
            ls.append(dict)
        return JsonResponse(ls, content_type="application/json", safe=False)
