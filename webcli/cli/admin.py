from django.contrib import admin
from cli.models import *



def make_active(modeladmin, request, queryset):
	queryset.update(active=True)
make_active.short_description = "Activate selected commands"

def make_inactive(modeladmin, request, queryset):
	queryset.update(active=False)
make_inactive.short_description = "Deactivate selected commands"

class CommandAdmin(admin.ModelAdmin):
	def _url(self, instance):
		truncated = instance.url[:64]
		return truncated if truncated == instance.url else truncated + '...'
	_url.short_description = "Url"

	def _title(self, instance):
			return f'<strong>{instance.title}</strong>' if instance.default else instance.title
	_title.allow_tags = True
	_title.short_description = "Title"

	def _active(self, instance):
		return instance.active
	_active.short_description = '👁'

	def _use_count(self, instance):
		return instance.use_count
	_use_count.short_description = 'Use'

	list_display = ('keyword', '_active', '_use_count', '_title', '_url', 'created_at', 'last_used')
	ordering = ['-default', '-active', '-use_count']
	actions = [make_active, make_inactive]
admin.site.register(Command, CommandAdmin)
