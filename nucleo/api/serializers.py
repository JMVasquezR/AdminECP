from rest_framework import serializers

from nucleo.models.tipo_documento import TipoDocumento


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'
