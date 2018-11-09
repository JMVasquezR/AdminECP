from django.conf.urls import url, include
from rest_framework import routers

from nucleo.api.views import *

router = routers.DefaultRouter()
router.register(r'tipo-documento', TipoDocumentoViewSet, base_name='tipo_documento')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'generos', listarGenerosViewSet.as_view(),name='genero'),
]
