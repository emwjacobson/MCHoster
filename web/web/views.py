from django.shortcuts import render, HttpResponse
import requests
import json

def get_endpoint(endpoint):
    res = requests.get(f'http://manager:5000/{endpoint}')
    return json.loads(res.text)

# Create your views here.
def index(request):
    return render(request, 'web/index.html', {})

def stats(request):
    try:
        res = get_endpoint('stats')
    except Exception as e:
        print(e)
        return render(request, 'web/stats.html', context={'stats': {'status': 'error', 'message': 'Error with backend manager'}})

    stats = {'stats': res, 'total_players': sum(ser['num_players'] for ser in res['servers'])}
    return render(request, 'web/stats.html', context=stats)