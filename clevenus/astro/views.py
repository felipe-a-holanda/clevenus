from django.shortcuts import render, get_object_or_404

from .models import *
from charts.views import chartNow
from users.models import UserProfile
def home(request):
    return chartNow(request)



def planet_view(request, planet):
    planet = get_object_or_404(Planet, slug=planet.lower())
    planet_in_signs = PlanetInSign.objects.filter(planet=planet).select_related('sign')
    params = dict()
    params['planet'] = planet
    params['planet_in_signs'] = planet_in_signs
    return render(request, 'astro/planet_view.html', params)


def sign_view(request, sign):
    sign = get_object_or_404(Sign, slug=sign.lower())
    planet_in_signs = PlanetInSign.objects.filter(sign=sign, planet__index__lt=10).select_related('planet')
    params = dict()
    params['sign'] = sign
    params['planet_in_signs'] = planet_in_signs
    return render(request, 'astro/sign_view.html', params)

def house_view(request, house):
    house = get_object_or_404(House, slug=house.lower())
    house_in_signs = HouseInSign.objects.filter(house=house).select_related('sign')
    planet_in_houses = PlanetInHouse.objects.filter(house=house, planet__index__lt=10).select_related('planet')
    params = dict()
    params['house'] = house
    params['planet_in_houses'] = planet_in_houses
    params['house_in_signs'] = house_in_signs
    return render(request, 'astro/house_view.html', params)


def planet_in_sign(request, planet, sign):
    planet_in_sign = get_object_or_404(PlanetInSign, planet__slug=planet, sign__slug=sign)
    params = dict()

    params['planet_in_sign'] = planet_in_sign
    params['charts'] = sorted(planet_in_sign.charts.all().select_related('user__user'))


    return render(request, 'astro/planet_in_sign.html', params)




def house_in_sign(request, house, sign):
    house_in_sign = get_object_or_404(HouseInSign, house__slug=house, sign__slug=sign)
    params = dict()

    params['house_in_sign'] = house_in_sign
    params['charts'] = sorted(house_in_sign.charts.all().select_related('user__user'))


    return render(request, 'astro/house_in_sign.html', params)


def planet_in_house(request, planet, house):
    planet_in_house = get_object_or_404(PlanetInHouse, planet__slug=planet, house__slug=house)
    params = dict()
    params['planet_in_house'] = planet_in_house
    params['charts'] = sorted(planet_in_house.charts.all().select_related('user__user'))
    return render(request, 'astro/planet_in_house.html', params)


def aspect(request, planet1, aspect_type, planet2):
    aspect = get_object_or_404(Aspect, p1__slug=planet1, type=aspect_type, p2__slug=planet2)

    params = dict()
    params['aspect'] = aspect
    params['charts'] = sorted(aspect.charts.filter(chartaspect__diff__lt=aspect.orb).select_related('user__user'))

    #sorted(aspect.charts.all().select_related('user__user'))
    return render(request, 'astro/aspect.html', params)
