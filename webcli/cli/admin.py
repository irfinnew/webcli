from django.contrib import admin
from cli.models import *



def make_active(modeladmin, request, queryset):
	queryset.update(active=True)
make_active.short_description = "Activate selected commands"

def make_inactive(modeladmin, request, queryset):
	queryset.update(active=False)
make_inactive.short_description = "Deactivate selected commands"

class CommandAdmin(admin.ModelAdmin):
	def admin_url(self, instance):
		if len(instance.url) > 64:
			return instance.url[:64] + '...'
		else:
			return instance.url
	admin_url.short_description = "Url"

	list_display = ('keyword', 'default', 'active', 'use_count', 'title', 'admin_url', 'created_at', 'last_used')
	ordering = ['default', 'active', 'use_count']
	actions = [make_active, make_inactive]
admin.site.register(Command, CommandAdmin)
