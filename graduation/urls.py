from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static

from GP import settings
from graduation.views import *
app_name = 'graduation'
urlpatterns = [
    # url(r'^$', landing_view, name='home'),
    url(r'^$', login_View, name='login'),
    url(r'^apply_for_supervisor$', apply_for_supervisor, name='apply_for_supervisor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
