from django.contrib import admin

from cli import models



def make_active(modeladmin, request, queryset):
	queryset.update(active=True)
make_active.short_description = "Activate selected commands"

def make_inactive(modeladmin, request, queryset):
	queryset.update(active=False)
make_inactive.short_description = "Deactivate selected commands"



@admin.register(models.Command)
class CommandAdmin(admin.ModelAdmin):
	def _url(self, instance):
		truncated = instance.url[:64]
		return truncated if truncated == instance.url else truncated + '...'
	_url.short_description = "Url"
	_url.admin_order_field = 'url'

	def _title(self, instance):
			return f'<strong>{instance.title}</strong>' if instance.default else instance.title
	_title.allow_tags = True
	_title.short_description = "Title"
	_title.admin_order_field = 'title'

	def _active(self, instance):
		return instance.active
	_active.short_description = '👁'
	_active.admin_order_field = 'active'
	_active.boolean = True

	def _use_count(self, instance):
		return instance.use_count
	_use_count.short_description = 'Use'
	_use_count.admin_order_field = 'use_count'

	list_display = ('keyword', '_active', '_use_count', '_title', '_url', 'created_at', 'last_used')
	ordering = ['-default', '-active', '-use_count']
	actions = [make_active, make_inactive]
