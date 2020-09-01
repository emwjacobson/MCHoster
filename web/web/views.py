from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
import requests
import json
from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings

def get_endpoint(endpoint):
    res = requests.get(f'http://manager/{endpoint}')
    return json.loads(res.text)

# Create your views here.
def index(request: WSGIRequest):
    print(request.path)
    return render(request, 'web/index.html', {})

def stats(request):
    try:
        res = get_endpoint('stats')
    except Exception as e:
        print(e)
        return render(request, 'web/stats.html', context={'stats': {'status': 'error', 'message': 'Error with backend manager'}})

    stats = {'stats': res, 'total_players': sum(ser['num_players'] for ser in res['servers'])}
    return render(request, 'web/stats.html', context=stats)

def start(request):
    try:
        username = request.POST['username']
        res = get_endpoint(f'start/{username}')
        return render(request, 'web/start.html', {'data': res, 'server_ip': settings.SERVER_IP})
    except KeyError as e:
        # If 'username' doesnt exist in post, render normal page
        return render(request, 'web/start.html', {})
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))

def manage(request):
    try:
        c_id = request.POST['c_id']
        print(request.POST)
        res = get_endpoint(f'stop/{c_id}')
        return render(request, 'web/manage.html', {'data': res})
    except KeyError as e:
        return render(request, 'web/manage.html', {})
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))
