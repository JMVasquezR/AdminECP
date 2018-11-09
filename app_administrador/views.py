from django.contrib.auth.views import LoginView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.views import APIView

from app_administrador.forms import LoginForm


class LoginUsiarioViewSet(LoginView):
    form_class = LoginForm
    template_name = 'usuario_login.html'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if hasattr(self.request.user,
                   'is_staff') and self.request.user.is_staff and self.request.user.is_active and not self.request.user.is_block:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('app_administrador:administrador_home')


class HomeViewSet(View):
    def get(self, request):
        return render(request, 'crear_cliente.html')
