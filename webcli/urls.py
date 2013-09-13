from django.conf.urls.defaults import *
from django.conf import settings
from django.views.static import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('cli.urls')),
	url(r'^_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
