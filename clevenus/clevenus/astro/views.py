from django.shortcuts import render, get_object_or_404

from .models import *
from charts.views import chartNow

def home(request):
    return chartNow(request)


def planet_in_sign(request, planet, sign):
    planet_in_sign = get_object_or_404(PlanetInSign, planet__slug=planet, sign__slug=sign)
    params = dict()
    params['planet_in_sign'] = planet_in_sign
    return render(request, 'astro/planet_in_sign.html', params)


def planet_in_house(request, planet, house):
    planet_in_house = get_object_or_404(PlanetInHouse, planet__slug=planet, house__slug=house)
    params = dict()
    params['planet_in_house'] = planet_in_house
    return render(request, 'astro/planet_in_house.html', params)


def aspect(request, planet1, aspect_type, planet2):
    aspect = get_object_or_404(Aspect, p1__slug=planet1, type=aspect_type, p2__slug=planet2)
    params = dict()
    params['aspect'] = aspect
    return render(request, 'astro/aspect.html', params)
