from django.contrib import admin
from django.urls import path, include
from django.conf import settings



urlpatterns = [
	path('', include('cli.urls')),
]
if settings.ADMIN_PATH:
	urlpatterns.append(path(settings.ADMIN_PATH, admin.site.urls))
