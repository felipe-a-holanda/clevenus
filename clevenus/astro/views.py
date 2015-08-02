from django.shortcuts import render, get_object_or_404

from .models import *
from charts.views import chartNow
from users.models import UserProfile
def home(request):
    return chartNow(request)



def planet_view(request, planet):
    planet = get_object_or_404(Planet, slug=planet.lower())
    planet_in_signs = PlanetInSign.objects.filter(planet=planet).select_related('sign').prefetch_related('positions')
    params = dict()
    params['planet'] = planet
    params['planet_in_signs'] = planet_in_signs
    return render(request, 'astro/planet_view.html', params)


def sign_view(request, sign):
    sign = get_object_or_404(Sign, slug=sign.lower())
    planet_in_signs = PlanetInSign.objects.filter(sign=sign, planet__index__lt=10).select_related('planet').prefetch_related('positions')
    params = dict()
    params['sign'] = sign
    params['planet_in_signs'] = planet_in_signs
    return render(request, 'astro/sign_view.html', params)


def planet_in_sign(request, planet, sign):
    planet_in_sign = get_object_or_404(PlanetInSign, planet__slug=planet, sign__slug=sign)
    params = dict()

    params['planet_in_sign'] = planet_in_sign
    params['users'] = sorted([u.chart.user for u in planet_in_sign.positions.all().select_related('chart__user__user__username')])


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
    params['users'] = sorted(set([u.chart.user for u in aspect.charts.all().select_related('chart__user')]))
    return render(request, 'astro/aspect.html', params)
