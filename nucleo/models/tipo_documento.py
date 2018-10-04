import re

from django.db import models

from nucleo.utilitarios.genericos import get_value_from_model_choice, CleanCharField

TIPO_PATRON = (
    (0, 'Numerico'),
    (1, 'Alfanumerico'),
)

TIPO_CONTRIBUYENTE = (
    (0, 'Documento para nacionales solamente'),
    (1, 'Documento para extranjeros solamente'),
    (2, 'Documento para nacionales y extranjeros'),
)

TIPO_LONGITUD = (
    (0, 'Exacta'),
    (1, 'Inexacta'),
)


class TipoDocumento(models.Model):
    nombre_corto = CleanCharField(blank=False, null=False, max_length=25)
    nombre_largo = CleanCharField(blank=False, null=False, max_length=100)
    tipo_patron = models.IntegerField(blank=False, null=False, choices=TIPO_PATRON)
    tipo_contribuyente = models.IntegerField(blank=False, null=False, choices=TIPO_CONTRIBUYENTE)
    tipo_longitud = models.IntegerField(blank=False, null=False, choices=TIPO_LONGITUD)
    longitud = models.IntegerField(blank=False, null=False, default=0)

    def _str_(self):
        return self.nombre_corto

    def validar_documento(self, codigo):

        """
        Funcion para la validacion del tipo de documento
        :param codigo: Es el codigo del documento
        :return:
        """

        if not self.is_valid_regex(self.tipo_patron, codigo):
            return False

        if not self.is_valid_longitud(self.tipo_longitud, self.longitud, codigo):
            return False

        return True

    def is_valid_regex(self, patron, codigo):
        """
        Funcion para la validacion del documento, alfanumero o numerico
        :param patron: Es la variable que define si el codigo es Numero o Alfanumerico
        :param codigo: Es el codigo del documento
        :return:
        """
        if patron == get_value_from_model_choice(TIPO_PATRON, 'Numerico'):
            expresion = re.compile(r'^([0-9]+)$')
        else:
            expresion = re.compile(r'^([\w]+)$')

        result = expresion.match(codigo)
        return bool(result)

    def is_valid_longitud(self, tipo_longitud, longitud, codigo):
        """
        Funcion para la validacion de la londitud del codugo de documento
        :param tipo_longitud: Variable que indica que tipo de longitud es
        :param longitud: Variable que indica la longitud del documento
        :param codigo: Es el codigo del documento
        :return:
        """
        if tipo_longitud == get_value_from_model_choice(TIPO_LONGITUD, 'Exacta'):
            return len(codigo) == longitud
        else:
            return len(codigo) <= longitud