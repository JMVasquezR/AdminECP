from django.conf.urls import url, include

from app_administrador.views import *

urlpatterns = [
    url(r'^login/', LoginUsiarioViewSet.as_view(), name='administrador_login'),
    url(r'^home/', HomeViewSet.as_view(), name='administrador_home'),
]