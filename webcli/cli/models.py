from django.db import models
import datetime

class Command(models.Model):
	keyword = models.CharField(max_length=32, unique=True)
	title = models.CharField(max_length=32)
	url = models.URLField()
	suggest_url = models.URLField(blank=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(default=datetime.datetime.now)
	last_used = models.DateTimeField(blank=True, null=True)
	use_count = models.IntegerField(default=0)
