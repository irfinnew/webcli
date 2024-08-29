from django.urls import path

from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('opensearch.xml', views.opensearch, name='opensearch'),
	path('cmd/<path:command>/', views.command, name='command'),
]
