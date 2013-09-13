from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('cli.views',
	url(r'^$', 'home', name='home'),
	url(r'^([A-Za-z0-9][A-Za-z0-9_-]*)$', 'command', name='command'),
	url(r'^([A-Za-z0-9][A-Za-z0-9_-]*) (.*)$', 'command', name='command'),
	url(r'^_admin/', include(admin.site.urls), name='admin'),
)
