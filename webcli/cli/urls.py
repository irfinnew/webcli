from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('cli.views',
	url(r'^$', 'home', name='home'),
	url(r'^([^ _][^ ]*)$', 'command', name='command'),
	url(r'^([^_ ][^ ]*) (.*)$', 'command', name='command'),
	url(r'^_admin/', include(admin.site.urls), name='admin'),
)
