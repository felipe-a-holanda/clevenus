from django.shortcuts import render, get_object_or_404

from django.views.generic.edit import UpdateView

from .models import UserProfile
from charts.models import Event
from django.views.generic.list import ListView
from charts.utils import ChartCalc

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django import forms
# Create your views here.



class UserListView(ListView):

    model = UserProfile


    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context




def user_profile_view(request, username):
    user = get_object_or_404(UserProfile, user__username=username)

    chart = user.chart
    chart.save()
    chart = ChartCalc(chart.datetime, chart.time, chart.lat, chart.lng)

    planets = chart.planets[:10]
    #aspects = [a for a in chart.aspects if a.diff<10 and a.p1.i<10 and a.p2.i<10]
    aspects = [a for a in chart.aspects if a.p1.i<10 and a.p2.i<10 and a.diff<a.aspect.orb]
    params = dict()

    asc = chart.asc
    #asc = 0
    params['asc'] = asc
    for p in planets:
        params.update(p.get_svg_params())


    params['user'] = user
    params['chart'] = chart
    params['houses'] = chart.houses
    params['planets'] = planets
    params['aspects'] = aspects
    params['action'] = '/chart/post'

    return render(request, 'charts/detail.html', params)



def user_profile_view_old(request, username):
    user = get_object_or_404(UserProfile, user__username=username)
    chart = user.chart

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




class UserForm(forms.Form):
    email = forms.EmailField(required=True, )

class UserCreate(UpdateView):
    model = UserProfile
    fields = ['date', 'time', 'city']

    def form_valid(self, form):
        return super(UserCreate, self).form_valid(form)

class SignUp(FormView):
   template_name = 'users/signup.html'
   form_class = UserForm
   success_url='/account'



   def form_valid(self, form):
      #save the new user first
      form.save()
      #get the username and password
      username = self.request.POST['username']
      password = self.request.POST['password1']
      #authenticate user then login
      user = authenticate(username=username, password=password)
      login(self.request, user)
      return super(SignUp, self).form_valid(form)