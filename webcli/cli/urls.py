from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('cli.views',
	url(r'^$', 'home', name='home'),
	url(r'^cmd/(.*)', 'command', name='command'),
	url(r'^admin/', include(admin.site.urls), name='admin'),
)
