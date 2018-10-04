from django.db import models

from nucleo.models.usuario_abstract import UsuarioAbstract


class Staff(UsuarioAbstract):
    foto = models.ImageField(upload_to='staff_fotos', blank=True, null=True)

    def get_extradata(self):
        return {'is_staff': True}

    #def after_user_create(self):
        #self.cuenta_de_usuario.inciar_activacion()