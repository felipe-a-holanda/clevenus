from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.transaction import atomic
# Create your views here.
from .models import Chart
from users.models import UserProfile
from interpretations.models import Interpretation
from interpretations.forms import InterpretationForm
from datetime import datetime
from django.utils import timezone

from .utils import ChartCalc
import pytz

def chartNow(request):
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    return chartDate(request, now)

def chartDate(request, date, time=None):
    print date,time
    date = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    if time:
        time = datetime.strptime(time, "%H:%M").time()
        date = datetime.combine(date, time).replace(tzinfo=timezone.utc)
    else:
        time = date.time()
    chart = ChartCalc(date, time)
    planets = chart.planets
    aspects = [a for a in chart.aspects if a.p1.i<10 and a.p2.i<10 and a.diff<a.aspect.orb]
    asc = chart.asc
    params = dict()

    params['datetime'] = date
    params['asc'] = asc
    for p in chart.planets:
        params.update(p.get_svg_params())
    params['chart'] = chart
    params['planets'] = [p for p in planets if p.i<10]
    params['aspects'] = aspects

    return render(request, 'charts/detail.html', params)



def chartView(request, chart_id):
    chart = get_object_or_404(Chart, pk=chart_id)

    chart = ChartCalc(chart.datetime, chart.time, chart.lat, chart.lng)


    planets = chart.planets
    aspects = [a for a in chart.aspects if a.p1.i<10 and a.p2.i<10 and a.diff<a.aspect.orb]
    params = dict()

    asc = chart.asc
    #asc = 0
    params['asc'] = asc
    for p in planets:
        params.update(p.get_svg_params())



    params['chart'] = chart
    params['houses'] = chart.houses

    params['planets'] = planets
    params['aspects'] = aspects
    params['action'] = '/chart/post'

    return render(request, 'charts/detail.html', params)







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
