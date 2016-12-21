from django.conf.urls import url
from django.contrib import admin
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', index),
    url(r'^event/(?P<p>\d+)', event, name='event'),
    url(r'^user_add/(?P<p>\d+)', add_user_event),
    url(r'^add_event$', add_event),
    url(r'^login$', auth.as_view(), name='login'),
    url(r'^reg$', reg.as_view(), name='reg'),
    url(r'^logout$', log, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
