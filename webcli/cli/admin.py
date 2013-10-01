from django.contrib import admin
from cli.models import *



class CommandAdmin(admin.ModelAdmin):
	def admin_url(self, instance):
		if len(instance.url) > 40:
			return instance.url[:40] + '...'
		else:
			return instance.url
	admin_url.short_description = "Url"

	list_display = ('keyword', 'title', 'admin_url', 'created_at', 'default', 'last_used', 'use_count')
admin.site.register(Command, CommandAdmin)
