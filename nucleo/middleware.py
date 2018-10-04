from abc import ABC, abstractclassmethod

from django.http.response import HttpResponseRedirect
from django.urls.base import resolve


class BaseMiddleware(ABC):
    def _init_(self, get_response, ls_urls_no_validadas, app_name, url_redireccion):
        self.get_response = get_response
        self.ls_urls_no_validadas = ls_urls_no_validadas
        self.app_name = app_name
        self.url_redireccion = url_redireccion

    def _call_(self, request):
        url = request.path
        url_resolved = resolve(url)

        if 'api' in url_resolved.namespaces:
            return self.get_response(request)

        if self.app_name == url_resolved.app_name and not url_resolved.url_name in self.ls_urls_no_validadas:
            if self.has_permission(request):
                return self.get_response(request)
            else:
                return HttpResponseRedirect(self.url_redireccion)

        else:
            return self.get_response(request)

    @abstractclassmethod
    def has_permission(self, request):
        pass