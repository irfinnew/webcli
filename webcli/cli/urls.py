from django.urls import path

from . import views


urlpatterns = [
	path(r'', views.home, name='home'),
	path(r'cmd/(.*)', views.command, name='command'),
	path(r'suggest/(.*)', views.suggest, name='suggest'),
]
