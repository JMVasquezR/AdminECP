from django.contrib import admin

from nucleo.models.staff import Staff
from nucleo.models.tipo_documento import TipoDocumento
from nucleo.models.usuario import Usuario

admin.site.register(Staff)
admin.site.register(Usuario)
admin.site.register(TipoDocumento)
