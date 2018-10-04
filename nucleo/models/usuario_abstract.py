from abc import abstractmethod

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from nucleo.models.tipo_documento import TipoDocumento
from nucleo.utilitarios.genericos import CleanCharField


def solo_texto(value):
    if not value.isspace():
        raise ValidationError(
            _('%(value)s debe contener solo letras'),
            params={'value': value},
        )


GENERO = (
    ('m', 'Masculino'),
    ('f', 'Femenino'),
)


class UsuarioAbstract(models.Model):
    class Meta:
        abstract = True

    cuenta_de_usuario = models.ForeignKey(get_user_model(), blank=True, on_delete=models.CASCADE)
    nombre = CleanCharField(blank=False, null=False, max_length=200)
    apellido_paterno = CleanCharField(blank=False, null=False, max_length=100)
    apellido_materno = CleanCharField(blank=True, null=False, max_length=100)
    fecha_de_nacimiento = models.DateField(blank=False, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, null=False, blank=False)
    numero_de_documento = CleanCharField(max_length=25, unique=True)
    genero = CleanCharField(blank=False, null=False, choices=GENERO, max_length=1)
    telefono_o_celular = CleanCharField(max_length=15)
    correo = models.EmailField(blank=False, null=False, unique=True)

    def _str_(self):
        return '%s, %s' % (self.nombre, self.apellido_paterno)

    @transaction.atomic()
    def save(self, **kwargs):
        if self.pk:
            self.update(**kwargs)
        else:
            self.create(**kwargs)

    @transaction.atomic()
    def create(self, **kwargs):
        extra_data_from_here = {
            'first_name': self.nombre,
            'last_name': '%s %s' % (self.apellido_paterno, self.apellido_materno),
        }
        extra_data_from_son = self.get_extradata()
        usuario = get_user_model().objects.create_user(
            self.correo,
            password=None,
            **({**extra_data_from_here, **extra_data_from_son})
        )
        self.cuenta_de_usuario = usuario
        super(UsuarioAbstract, self).save(**kwargs)
        self.after_user_create()

    @transaction.atomic()
    def update(self, **kwargs):
        self.cuenta_de_usuario.first_name = self.nombre
        self.cuenta_de_usuario.last_name = '%s %s' % (self.apellido_paterno, self.apellido_materno)
        self.cuenta_de_usuario.save()
        super(UsuarioAbstract, self).save(**kwargs)

    @abstractmethod
    def get_extradata(self):
        '''
        :return:(dict)
        '''
        pass

    @abstractmethod
    def after_user_create(self):
        pass
