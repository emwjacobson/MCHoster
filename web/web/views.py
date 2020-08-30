from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
import requests
import json
from django.core.handlers.wsgi import WSGIRequest

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
        print(res)
        return render(request, 'web/start.html', {'view': 'response', 'data': res})
    except KeyError as e:
        # If 'username' doesnt exist in post, render normal page
        return render(request, 'web/start.html', {'view': 'normal'})
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))