from rest_framework import serializers

from nucleo.models.cliente import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'correo',
            'fecha_de_nacimiento',
            'genero',
            'tipo_documento',
            'numero_de_documento',
            'telefono_o_celular',
        )
