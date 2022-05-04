from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include('api.urls')),
]
