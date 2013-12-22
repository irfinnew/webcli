from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
import datetime
from models import *
import urllib



# Returns 4-tuple: (command, keyword, args, command object)
# If the specified command does not exist, and no default command exists, raises a 404.
def parse_command(command):
	# UGLY HACK: nginx doesn't unquote the url so we do it here. Fuck nginx.
	command = urllib.unquote(command)

	path = command.split(' ')
	keyword = path[0]
	args = ' '.join(path[1:])

	try:
		cmd = Command.objects.get(keyword=keyword)
	except ObjectDoesNotExist:
		cmd = Command.objects.get(default=True)
		keyword = ''
		args = command

	return (command, keyword, args, cmd)

	

def home(request):
	commands = Command.objects.all().order_by('-use_count')

	most = commands[0].use_count
	for c in commands:
		if c.use_count >= most / 20 and c.use_count > 0:
			c.popular = True
		elif c.use_count >= most / 200 and c.use_count > 0:
			c.common = True

	return render_to_response('home.html',
		{
			'commands': commands,
		}, context_instance=RequestContext(request))



def command(request, command):
	(command, keyword, args, cmd) = parse_command(command)

	cmd.last_used = datetime.datetime.now()
	cmd.use_count += 1
	cmd.save()

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
