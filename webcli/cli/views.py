from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
import datetime
from models import *
import urllib



def home(request):
	commands = Command.objects.all().order_by('-use_count')

	return render_to_response('home.html',
		{
			'commands': commands,
		}, context_instance=RequestContext(request))



def command(request, command):
	# UGLY HACK: nginx doesn't unquote the url so we do it here. Fuck nginx.
	path = urllib.unquote(command).split(' ')
	keyword = path[0]
	args = ' '.join(path[1:])

	cmd = get_object_or_404(Command, keyword=keyword)

	cmd.last_used = datetime.datetime.now()
	cmd.use_count += 1
	cmd.save()

	return HttpResponseRedirect(cmd.url.replace('%s', args))



def suggest(request, command):
	# UGLY HACK: nginx doesn't unquote the url so we do it here. Fuck nginx.
	path = urllib.unquote(command).split(' ')
	keyword = path[0]
	args = ' '.join(path[1:])

	cmd = get_object_or_404(Command, keyword=keyword)
	if not cmd.suggest_url:
		raise Http404

	# Hack: keyword is included in suggest request. It has to be, otherwise
	# the client will reject the response as not matching their query.
	# The only other way is to fetch the suggestions ourselves and modify
	# the response, but that probably means blocking webCLI for all users...
	return HttpResponseRedirect(cmd.suggest_url.replace('%s', command))
