from django.urls.base import reverse

from nucleo.middleware import BaseMiddleware


class AdministradorMiddleware(BaseMiddleware):
    def _init_(self, get_response):
        super(AdministradorMiddleware, self)._init_(
            get_response=get_response,
            ls_urls_no_validadas=['administrador_login', 'administrador_home', ],
            app_name='app_administrador',
            url_redireccion=reverse('app_administrador:administrador_login')
        )

    def has_permission(self, request):
        if request.user.is_anonymous:
            return False
        return request.user.is_active and request.user.is_staff