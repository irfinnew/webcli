# webcli - A command-line interface to the web.
#
# Copyright 2013-2022 Marcel Moreaux
# Licensed under BSD 3-clause. See LICENSE for details.

import datetime

from django.db import models



class Command(models.Model):
	class Meta:
		ordering = ['keyword']

	keyword = models.CharField(max_length=32, unique=True)
	active = models.BooleanField(default=True)
	default = models.BooleanField(default=False)
	title = models.CharField(max_length=32)
	url = models.URLField()
	suggest_url = models.URLField(blank=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(default=datetime.datetime.now)
	last_used = models.DateTimeField(blank=True, null=True)
	use_count = models.IntegerField(default=0)

	def __str__(self):
		return self.keyword
