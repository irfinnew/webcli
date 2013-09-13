from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import datetime
from models import *



def home(request):
	commands = Command.objects.all().order_by('-use_count')

	return render_to_response('home.html',
		{
			'commands': commands,
		}, context_instance=RequestContext(request))



def command(request):
	path = request.path.split(' ')
	keyword = path[0][1:]
	args = ' '.join(path[1:])
	cmd = get_object_or_404(Command, keyword=keyword)

	cmd.last_used = datetime.datetime.now()
	cmd.use_count += 1
	cmd.save()

	return HttpResponseRedirect(cmd.url.replace('%s', args))
