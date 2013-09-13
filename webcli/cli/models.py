from django.db import models
import datetime

class Command(models.Model):
	keyword = models.SlugField(unique=True)
	title = models.CharField(max_length=32)
	url = models.URLField()
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(default=datetime.datetime.now)
	last_used = models.DateTimeField(blank=True, null=True)
	use_count = models.IntegerField(default=0)
