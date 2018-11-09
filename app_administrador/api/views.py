from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app_administrador.api.serializers import ClienteSerializer
from nucleo.models.cliente import Cliente


class ClienteViewSet(mixins.CreateModelMixin, GenericViewSet):
    '''Esta vista es para que el Staff pueda crear Nana en estado basico'''
    # permission_classes = (StaffGeneralPermission,)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        a = ''
        return super().create(request, *args, **kwargs)

