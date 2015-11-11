from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .utils import gen_dict
import json

def get_data(request, p1_code, p2_code):
    from charts.utils import CONSTS
    planets = {p.code: p for i, p in CONSTS.planets.iteritems()}
    p1 = planets[p1_code]
    p2 = planets[p2_code]

    rev = min(p1.revolution, p2.revolution)/2
    data = gen_dict(p1, p2, rev)
    output = json.dumps(data, indent=4)
    return HttpResponse(output, content_type="application/json")
    #return JsonResponse(data)

# Create your views here.
