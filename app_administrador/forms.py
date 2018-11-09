from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"type": "email", "name": "username", "autocomplete": "username", "id": "username",
               "placeholder": "Ingrese Correo Electronico", "class": "form-control", 'autofocus': "autofocus"}),
        required=True)
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={"type": "password", "name": "password", "id": "password", "placeholder": "Ingrese Contraseña",
                   "class": "form-control"}), required=True)

    def confirm_login_allowed(self, user):
        if not user.is_staff or user.is_block or not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        else:
            pass
            # valanti_data = Valanti(nana=Nana.objects.get(cuenta_de_usuario=user))
            # valanti_data.save()
