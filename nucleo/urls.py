from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('nucleo.api.urls', namespace='api')),
]
