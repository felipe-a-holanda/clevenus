import operator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import *
from charts.views import chartNow, soon
import itertools
from datetime import datetime
from datetime import timedelta

def home(request):
    return soon(request)
    #return chartNow(request)

def search_view(request):
    terms = request.GET['search'].split()
    q_list = [Q(iname__icontains=term) for term in terms]
    query = reduce(operator.and_, q_list[1:], q_list[0])

    objs = itertools.chain(*[Model.objects.filter(query) for Model in (Sign, Planet, House, PlanetInSign, PlanetInHouse, HouseInSign, Aspect)])
    return render(request, 'astro/search.html', {'terms':terms, 'objs':objs})


def planet_view(request, planet):
    planet = get_object_or_404(Planet, slug=planet.lower())
    planet_in_signs = PlanetInSign.objects.filter(planet=planet).select_related('sign').prefetch_related('charts')
    positions = list()
    for d in planet.get_positions():

        c = d['angle'] % 120
        if 0 <= c <30:
            d['color'] ='#ff0000'
        if 30 <= c <60:
            d['color'] ='#00ff00'
        if 60 <= c <90:
            d['color'] ='#ffff00'
        if 90 <= c <120:
            d['color'] ='#0000ff'
        d['date'] = d['date'].strftime('%Y-%m-%d')
        d['angle'] = d['angle']

        positions.append(d)
    #positions = [{'color':'#b7e021', 'date':d.strftime('%Y-%m-%d'), 'angle':int(a)} for d, a in planet.get_positions()]
    #print positions


    today = datetime.today()
    period = timedelta(days=30)
    start_date = today - period
    end_date = today + period
    format = "Date(%Y, %-m, %-d)"
    params = dict()
    params['planet'] = planet
    params['planet_in_signs'] = planet_in_signs
    params['positions'] = positions
    params['start_date'] = start_date.strftime(format)
    params['end_date'] = end_date.strftime(format)
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

from api.utils import ASPECTS
def aspect(request, planet1, aspect_type, planet2):
    Q1 = Q(p1__slug=planet1, type=aspect_type, p2__slug=planet2)
    Q2 = Q(p2__slug=planet1, type=aspect_type, p1__slug=planet2)
    aspects = Aspect.objects.filter(Q1 | Q2)
    if aspects:
        aspect = aspects.first()

    p1 = aspect.p1
    p2 = aspect.p2
    params = dict()
    params['aspect'] = aspect
    params['charts'] = sorted(aspect.charts.filter(chartaspect__diff__lt=aspect.orb).select_related('user__user'))
    params['orb'] = 1
    params['aspects'] = ASPECTS
    params['today'] = datetime.now().strftime('%Y-%m-%d')
    params['p1'] = p1
    params['p2'] = p2
    params['data_url'] = reverse('api-aspect', args=(p1.code, p2.code))

    #sorted(aspect.charts.all().select_related('user__user'))
    return render(request, 'astro/aspect.html', params)
