from django.conf.urls import url, include
from rest_framework import routers

from app_administrador.api.views import *

router = routers.DefaultRouter()
router.register(r'cliente', ClienteViewSet, base_name='cliente')

urlpatterns = router.urls
