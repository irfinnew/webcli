from django.contrib import admin
from cli.models import *



class CommandAdmin(admin.ModelAdmin):
	list_display = ('keyword', 'title', 'url', 'created_at', 'last_used', 'use_count')
admin.site.register(Command, CommandAdmin)
