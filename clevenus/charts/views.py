from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.transaction import atomic

import re
# Create your views here.
from .models import Chart
from users.models import UserProfile

from interpretations.forms import InterpretationForm
from datetime import datetime, timedelta
from django.utils import timezone
from charts.models import Event
from django.views.generic.list import ListView

from .utils import ChartCalc
from .models import City
import pytz


def soon(request):
    return render('charts/soon.html')

def chartNow(request):
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    date = now.date()
    time = now.time()


    return chartDate(request, date.strftime('%Y-%m-%d'), time.strftime('%H:%M'))



def parse_coords(coords):
    lat = lng = None
    if coords:
        try:
            groups = re.match(r'([\-\+]?[0-9]*(\.[0-9]+)?)\s*,\s*([\-\+]?[0-9]*(\.[0-9]+)?)', coords).groups()
            lat, _, lng, __ = groups
            lat = float(lat)
            lng = float(lng)
        except:
            lat = lng = None
    return lat, lng




def generate_timdelta_urls(datetime_utc, city_name=None):
    date_format = '%Y-%m-%d/%H:%M'

    url_minus_minute = reverse('chart_datetime', args=((datetime_utc - timedelta(minutes=1)).strftime(date_format), ))
    url_plus_minute = reverse('chart_datetime', args=((datetime_utc + timedelta(minutes=1)).strftime(date_format), ))

    url_minus_hour = reverse('chart_datetime', args=((datetime_utc - timedelta(hours=1)).strftime(date_format), ))
    url_plus_hour = reverse('chart_datetime', args=((datetime_utc + timedelta(hours=1)).strftime(date_format), ))

    url_minus_day = reverse('chart_datetime', args=((datetime_utc - timedelta(days=1)).strftime(date_format), ))
    url_plus_day = reverse('chart_datetime', args=((datetime_utc + timedelta(days=1)).strftime(date_format), ))

    url_minus_week = reverse('chart_datetime', args=((datetime_utc - timedelta(days=7)).strftime(date_format), ))
    url_plus_week = reverse('chart_datetime', args=((datetime_utc + timedelta(days=7)).strftime(date_format), ))

    url_minus_month = reverse('chart_datetime', args=((datetime_utc - timedelta(days=30)).strftime(date_format), ))
    url_plus_month = reverse('chart_datetime', args=((datetime_utc + timedelta(days=30)).strftime(date_format), ))

    url_minus_year = reverse('chart_datetime', args=((datetime_utc - timedelta(days=365)).strftime(date_format), ))
    url_plus_year = reverse('chart_datetime', args=((datetime_utc + timedelta(days=365)).strftime(date_format), ))
    return locals()
    #return createDict(locals())

def chartDate(request, date, time=None, city_name=None):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        if time:
            try:
                time = datetime.strptime(time, "%H:%M").time()
            except:
                time = datetime.strptime(time, "%H:%M:%S").time()
            date = datetime.combine(date, time).replace(tzinfo=timezone.utc)
        else:
            date = date.replace(hour=12)
            time = date.time()
    except:
        date_time = datetime.strptime(date, '%Y-%m-%d/%H:%M').replace(tzinfo=timezone.utc)
        date = date_time
        time = date_time.time()
    datetime_utc = date.replace(tzinfo=None)

    lat = lng = None
    if city_name:
        try:
            city = City.create(city_name)
            lat = city.lat
            lng = city.lng
        except:
            lat = lng = None

    chart = ChartCalc(date, time, lat, lng)
    planets = chart.planets
    aspects = [a for a in chart.aspects if a.p1.i<10 and a.p2.i<10 and a.diff<a.aspect.orb]
    asc = chart.asc
    params = dict()





    #{% url 'chart_datetime' datetime_utc|timedelta:'-1 minutes'|date:'Y-m-d/H:i' %}
    params.update(generate_timdelta_urls(datetime_utc, city_name))
    params['city_name'] = city_name
    params['datetime'] = date
    params['datetime_utc'] = datetime_utc
    params['datetime_now_utc'] = datetime.utcnow().replace(tzinfo=None)
    params['date'] = date.date()
    params['time'] = date.time()
    params['asc'] = asc
    for p in chart.planets:
        params.update(p.get_svg_params())
    params['chart'] = chart
    params['planets'] = [p for p in planets if p.i<10]
    params['aspects'] = aspects
    params['houses'] = chart.houses


    return render(request, 'charts/chart_date.html', params)



def chartView(request, username):
    user = get_object_or_404(UserProfile, username=username)
    chart_obj = user.birth.chart
    chart = ChartCalc(chart_obj.datetime, chart_obj.time, chart_obj.lat, chart_obj.lng)


    planets = chart.planets
    aspects = [a for a in chart.aspects if a.p1.i<10 and a.p2.i<10 and a.diff<a.aspect.orb]
    params = dict()

    asc = chart.asc
    #asc = 0
    params['asc'] = asc
    for p in planets:
        params.update(p.get_svg_params())



    params['chart'] = chart_obj
    params['houses'] = chart.houses

    params['planets'] = planets
    params['aspects'] = aspects
    params['action'] = '/chart/post'

    return render(request, 'charts/detail.html', params)


def transits(request, username):
    user = get_object_or_404(UserProfile, username=username)
    chart = user.birth.chart

    start = datetime.now() - timedelta(days=90)
    end = datetime.now() + timedelta(days=366)
    dates = [start + timedelta(days=x) for x in range(0, (end-start).days)]

    #for date in dates:
    #    print(date)
    positions = [{'date':datetime(2015,11,1), 'angle':0.5}, {'date':datetime(2015,11,10), 'angle':0.7}, {'date':datetime(2015,11,20), 'angle':0.3}]

    params = dict()
    params['userprofile'] = user
    params['positions'] = positions
    return render(request, 'charts/transits.html', params)





def chartView_old(request, chart_id):
    chart = get_object_or_404(Chart, pk=chart_id)

    planets = chart.planetposition_set.all().select_related('planet',  'sign', 'house')[:10]
    aspects = chart.chartaspect_set.filter(diff__lt=10, p1__planet__index__lt=10, p2__planet__index__lt=10).select_related('p1__planet', 'p2__planet', 'aspect')
    params = dict()

    asc = chart.house_1
    #asc = 0
    params['asc'] = asc
    for p in planets:
        params.update(p.get_svg_params())



    params['chart'] = chart

    params['planets'] = planets
    params['aspects'] = aspects
    params['action'] = '/chart/post'

    return render(request, 'charts/detail.html', params)




def postIntepretation(request):
    # A POST request: Handle Form Upload
    form = InterpretationForm(request.POST) # Bind data from request.POST into a PostForm

    # If data is valid, proceeds to create a new post and redirect the user
    if form.is_valid():
        text = form.cleaned_data['text']
        chart = form.cleaned_data['chart']
        obj = form.cleaned_data['obj']
        i = Interpretation.objects.create(text=text, chart=chart, obj=obj, user=1)
        i.save()
        return HttpResponse('ok')

class EventListView(ListView):

    model = Event
    queryset = Event.objects.select_related('chart', 'city').order_by('name')

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        return context
