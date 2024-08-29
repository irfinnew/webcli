# webcli - A command-line interface to the web.
#
# Copyright 2013-2022 Marcel Moreaux
# Licensed under BSD 3-clause. See LICENSE for details.

import urllib

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils import timezone

from cli.models import Command



# Returns 4-tuple: (command, keyword, args, command object)
# If the specified command does not exist, and no default command exists, raises a 404.
def parse_command(command):
	command = command.replace('+', ' ')
	path = command.split(' ')
	keyword = path[0]
	args = ' '.join(path[1:])

	try:
		cmd = Command.objects.prefetch_related('overrides').get(keyword=keyword, active=True)
	except ObjectDoesNotExist:
		cmd = Command.objects.get(default=True)
		keyword = ''
		args = command

	return (command, keyword, args, cmd)



def home(request):
	commands = Command.objects.filter(active=True).order_by('-use_count')

	most = commands[0].use_count
	for c in commands:
		if c.use_count >= most / 20 and c.use_count > 1000:
			c.popular = True
		elif c.use_count >= most / 200 and c.use_count > 100:
			c.common = True

	return render(request, 'home.html', {'commands': commands})



def opensearch(request):
	return render(request, 'opensearch.xml', {'hostname': request.get_host()},
		content_type='application/opensearchdescription+xml')



def bookmark(request, cmd):
	return render(request, 'bookmark.html', {'cmd': cmd})



def command(request, command):
	(command, keyword, args, cmd) = parse_command(command)

	cmd.last_used = timezone.now()
	cmd.use_count += 1
	cmd.save()

	for override in cmd.overrides.all():
		if override.argument == args:
			return HttpResponseRedirect(override.url)

	if not args and cmd.empty_url:
		return HttpResponseRedirect(cmd.empty_url)

	if not cmd.url:
		return bookmark(request, cmd)

	return HttpResponseRedirect(cmd.url.replace('%s', args))



def suggest(request, command):
	(command, keyword, args, cmd) = parse_command(command)

	if not cmd.suggest_url:
		raise Http404

	# Hack: keyword is included in suggest request. It has to be, otherwise
	# the client will reject the response as not matching their query.
	# The only other way is to fetch the suggestions ourselves and modify
	# the response, but that probably means blocking webCLI for all users...
	return HttpResponseRedirect(cmd.suggest_url.replace('%s', command))
