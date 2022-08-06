from django.urls import path

from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('cmd/<command>/', views.command, name='command'),
	path('suggest/<command>/', views.suggest, name='suggest'),
]
