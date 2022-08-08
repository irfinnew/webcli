from django.urls import path

from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('cmd/<path:command>/', views.command, name='command'),
	path('suggest/<path:command>/', views.suggest, name='suggest'),
]
