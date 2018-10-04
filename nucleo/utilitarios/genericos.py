import random
import re
import string
from collections import OrderedDict

from django.db import models


def generate_random_password(length=8):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_value_from_model_choice(tuple_of_choices, key):
    '''
    Este metodo se encargara de obtener el valor de la clave de un choice para djnago models
    :param tuple_of_choices:
    :param key:
    :return:
    '''
    for item in tuple_of_choices:
        if item[1] == key:
            return item[0]
    raise Exception('Clave no encontrada')



def get_key_with_value_from_model_choice(tuple_of_choices, value):
    for item in tuple_of_choices:
        if item[0] == value:
            return item[1]
    raise Exception('Valor no encontrado')


def get_dict_with_choices(tuple_of_choices):
    '''
    Este metodo recibe una tupla de choices y los convierte en un diccionario ordenado
    :param tuple_of_choices:
    :return:
    '''
    dict = {}
    for i in tuple_of_choices:
        key = str(i[1])
        dict[key] = i[0]
    dict = OrderedDict(sorted(dict.items(), key=lambda t: t[1]))
    return dict


def clean_text(text):
    if text:
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        return text
    else:
        return ''


class CleanCharField(models.CharField):
    def get_prep_value(self, value):
        return clean_text(super(CleanCharField, self
                                ).get_prep_value(value))

    def pre_save(self, model_instance, add):
        return clean_text(super(CleanCharField, self
                                ).pre_save(model_instance, add))


from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name