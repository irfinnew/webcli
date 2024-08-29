# webcli - A command-line interface to the web.
#
# Copyright 2013-2022 Marcel Moreaux
# Licensed under BSD 3-clause. See LICENSE for details.

from django.db import models
from django.utils import timezone



class Command(models.Model):
	class Meta:
		ordering = ['keyword']

	keyword = models.CharField(max_length=32, unique=True, help_text='This is the keyword that starts a command.')
	active = models.BooleanField(default=True, help_text='Whether the command can actually be used and is shown on the home page.')
	default = models.BooleanField(default=False, help_text='When true, this command is used if an incoming request doesn\'t match any command.')
	title = models.CharField(max_length=32, help_text='Displayed on the home page to identify/explain the command.')
	url = models.URLField(blank=True, help_text='The command is redirected to this URL. <code>%s</code> in the URL is replaced with the command argument.')
	empty_url = models.URLField(blank=True, help_text='If specified, this URL is used when the command is invoked without arguments.')
	suggest_url = models.URLField(blank=True, help_text='URL for suggesting completions. Not sure this even works anymore...')
	created_at = models.DateTimeField(default=timezone.now)
	last_used = models.DateTimeField(blank=True, null=True)
	use_count = models.IntegerField(default=0, help_text='How often this command was invoked. Used to style the home page.')

	def __str__(self):
		return self.keyword



class Override(models.Model):
	command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name='overrides')
	argument = models.CharField(blank=True, max_length=32)
	title = models.CharField(max_length=64)
	url = models.URLField(help_text='The command is redirected to this URL. <code>%s</code> in the URL is replaced with the command argument.')

	def __str__(self):
		return self.title
