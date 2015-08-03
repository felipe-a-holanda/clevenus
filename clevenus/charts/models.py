from datetime import datetime, time
import geocoder
import geopy
import pytz
from timezone_field import TimeZoneField
#import swisseph as swe
#swe.set_ephe_path('/usr/share/libswe/ephe/')

from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from astro.models import Aspect, Planet, Sign, House, PlanetInHouse, PlanetInSign, HouseInSign
from users.models import UserProfile
from math import pi, sin, cos
from .utils import ChartCalc, CONSTS



class City(models.Model):
    name = models.CharField(max_length=512)
    city = models.CharField(max_length=512)
    state = models.CharField(max_length=512)
    country = models.CharField(max_length=512)
    lat = models.FloatField()
    lng = models.FloatField()
    timezone = TimeZoneField()

    @classmethod
    def create(cls, city_name):
        city = City(name=city_name)
        city.geocode()
        existent = City.objects.filter(name=city.name, lat=city.lat, lng=city.lng)
        if existent:
            return existent.first()
        else:
            city.save()
            return city

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.geocode()
        super(City, self).save(*args, **kwargs)

    def geocode(self):
        g = geocoder.google(self.name)


        if g.ok:
            self.name = g.address
            self.city = g.city
            self.state = g.state
            self.country = g.country
            self.lat = g.lat
            self.lng = g.lng
            t = geopy.GoogleV3()
            self.timezone = t.timezone((self.lat, self.lng))
        else:
            print self.name, g



class ChartAspect(models.Model):
    name = models.CharField(max_length=256)
    chart = models.ForeignKey('Chart')
    aspect = models.ForeignKey(Aspect, related_name='chart_aspects')
    angle = models.FloatField()
    exact = models.FloatField()
    diff = models.FloatField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "%s %.1f" % (self.aspect.name, self.diff)
        super(ChartAspect, self).save(*args, **kwargs)




class Chart(models.Model):
    #user = models.ForeignKey(UserProfile, related_name='charts')
    name = models.CharField(max_length=256)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    datetime = models.DateTimeField()
    city = models.ForeignKey(City, null=True, blank=True)
    city_name = models.CharField(max_length=512, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    sun = models.FloatField(_('Sun'))
    moon = models.FloatField(_('Moon'))
    mercury = models.FloatField(_('Mercury'))
    venus = models.FloatField(_('Venus'))
    mars = models.FloatField(_('Mars'))
    jupiter = models.FloatField(_('Jupiter'))
    saturn = models.FloatField(_('Saturn'))
    uranus = models.FloatField(_('Uranus'))
    neptune = models.FloatField(_('Neptune'))
    pluto = models.FloatField(_('Pluto'))
    mean_node = models.FloatField()
    true_node = models.FloatField()
    mean_apog = models.FloatField()
    oscu_apog = models.FloatField()
    earth = models.FloatField()
    chiron = models.FloatField()
    pholus = models.FloatField()
    ceres = models.FloatField()
    pallas = models.FloatField()
    juno = models.FloatField()
    vesta = models.FloatField()
    intp_apog = models.FloatField()
    intp_perg = models.FloatField()

    house_1 = models.FloatField(null=True, blank=True)
    house_2 = models.FloatField(null=True, blank=True)
    house_3 = models.FloatField(null=True, blank=True)
    house_4 = models.FloatField(null=True, blank=True)
    house_5 = models.FloatField(null=True, blank=True)
    house_6 = models.FloatField(null=True, blank=True)
    house_7 = models.FloatField(null=True, blank=True)
    house_8 = models.FloatField(null=True, blank=True)
    house_9 = models.FloatField(null=True, blank=True)
    house_10 = models.FloatField(null=True, blank=True)
    house_11 = models.FloatField(null=True, blank=True)
    house_12 = models.FloatField(null=True, blank=True)


    planets_in_signs = models.ManyToManyField(PlanetInSign, related_name='charts')
    planets_in_houses = models.ManyToManyField(PlanetInHouse, related_name='charts')
    houses_in_signs = models.ManyToManyField(HouseInSign, related_name='charts')
    aspects = models.ManyToManyField(Aspect, through='ChartAspect', related_name='charts')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    @classmethod
    def create(cls, name, date, time=None, city=None):
        chart = Chart(name=name, date=date, time=time, city=city)
        chart.save()
        return chart


    @transaction.atomic
    def save(self, *args, **kwargs):
        self.update_datetime_city()

        self.chart_calc = ChartCalc(self.datetime, self.time, self.lat, self.lng)
        self.calculate()
        super(Chart, self).save()
        self.create_relations()

    def calculate(self):
        for p in self.chart_calc.planets:
            setattr(self, p.code, p.x)
        if self.chart_calc.houses:
            for i, h in enumerate(self.chart_calc.houses):
                setattr(self, 'house_%d' % i, h.angle)


    def create_relations(self):
        self.planets_in_signs.clear()
        self.planets_in_houses.clear()
        self.houses_in_signs.clear()
        self.aspects.clear()

        self.planets_in_signs.add(*[i.planet_in_sign for i in self.chart_calc.planets])
        if self.chart_calc.houses:
            self.planets_in_houses.add(*[i.planet_in_house for i in self.chart_calc.planets])
            self.houses_in_signs.add(*[i.house_in_sign for i in self.chart_calc.houses])

        for aspect in self.chart_calc.aspects:
            c = ChartAspect(chart=self, aspect=aspect.aspect, angle=aspect.angle, exact=aspect.exact, diff=aspect.diff)
            c.save()

        #self.aspects.add(*[i.aspect for i in self.chart_calc.aspects])


    def update_datetime_city(self):
        if self.time:
            self.datetime = datetime.combine(self.date, self.time)
            if self.city:
                self.datetime = self.city.timezone.localize(self.datetime)
                self.city_name = self.city.name
                self.lat = self.city.lat
                self.lng = self.city.lng
            else:
                self.datetime = pytz.utc.localize(self.datetime)
        else:
            self.datetime = datetime.combine(self.date, time(12, 0))
            self.datetime = pytz.utc.localize(self.datetime)