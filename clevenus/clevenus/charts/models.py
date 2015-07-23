from datetime import datetime, time
import geocoder
import pytz
from tzwhere.tzwhere import tzwhere
tzwhere = tzwhere()
from timezone_field import TimeZoneField
import swisseph as swe
swe.set_ephe_path('/usr/share/libswe/ephe/')

from django.db import models
from django.utils.translation import ugettext_lazy as _

from astro.models import Aspect, Planet, Sign, House, PlanetInHouse, PlanetInSign, HouseInSign
from users.models import UserProfile
from math import pi, sin, cos

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
            self.timezone = tzwhere.tzNameAt(self.lat, self.lng)
        else:
            print self.name, g


class PlanetPosition(models.Model):
    name = models.CharField(max_length=256)
    chart = models.ForeignKey('Chart')
    planet = models.ForeignKey(Planet)
    sign = models.ForeignKey(Sign)
    asc = models.FloatField(default=0)
    house = models.ForeignKey(House, null=True, blank=True)
    angle = models.FloatField()
    speed = models.FloatField()
    planet_in_sign = models.ForeignKey(PlanetInSign)
    planet_in_house = models.ForeignKey(PlanetInHouse, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.house:
            self.name = "%s %.1f %s (%s)" % (self.planet.name, self.angle % 30, self.sign.name, self.house.name)
        else:
            self.name = "%s %.1f %s" % (self.planet.name, self.angle % 30, self.sign.name)

        super(PlanetPosition, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_x(self, planet_radius=220, chart_center_x=300):
        x = cos((self.angle+180-self.asc)*pi/180.0) * planet_radius + chart_center_x
        return x

    def get_y(self, planet_radius=220, chart_center_y=300):
        y = -sin((self.angle+180-self.asc)*pi/180.0) * planet_radius + chart_center_y
        return y

    def get_x_aspect(self):
        return self.get_x(planet_radius=200)

    def get_y_aspect(self):
        return self.get_y(planet_radius=200)

    def get_chart_params(self, planet_radius=220, planet_size=7, planet_circle=10):
        params = dict()
        planet_scale = planet_size*2/100.0
        chart_center_x = 300
        chart_center_y = 300
        p_x = self.get_x()
        p_y = self.get_y()

        visibility = True
        params[self.planet.code+'_visibility'] = 'visible' if visibility else 'hidden'
        params[self.planet.code+'_x'] = p_x
        params[self.planet.code+'_y'] = p_y
        params[self.planet.code+'_circle'] = planet_circle
        params[self.planet.code+'_scale'] = planet_scale

        params[self.planet.code+'_x_corner'] = p_x - planet_size
        params[self.planet.code+'_y_corner'] = p_y - planet_size
        return params


class ChartAspect(models.Model):
    name = models.CharField(max_length=256)
    chart = models.ForeignKey('Chart')
    aspect = models.ForeignKey(Aspect)
    angle = models.FloatField()
    exact = models.FloatField()
    diff = models.FloatField()
    p1 = models.ForeignKey(PlanetPosition, verbose_name='First Planet', related_name='chart_aspects_first')
    p2 = models.ForeignKey(PlanetPosition, verbose_name='Second Planet', related_name='chart_aspects_second')
    asc = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "%s %.1f" % (self.aspect.name, self.diff)
        super(ChartAspect, self).save(*args, **kwargs)

    @classmethod
    def create(cls, chart, pi1, pi2, p1, p2, asc=0):
        a1 = p1.angle
        a2 = p2.angle

        angle = min(abs(a1-a2), abs(360 - abs(a1-a2)))
        a, b = divmod(angle, 30)
        c, d = map(abs, divmod(angle, -30))
        diff, exact = min((b, a), (d, c))
        exact *= 30
        exact = int(exact)
        if exact==30 or exact==150:
            return None

        #p1 = Planet.objects.get(index=pi1)
        #p2 = Planet.objects.get(index=pi2)
        aspect = Aspect.objects.get(p1=p1.planet, p2=p2.planet, degrees=int(exact))
        chartAspect = cls(chart=chart, p1=p1, p2=p2, diff=diff, exact=exact, angle=angle, aspect=aspect, asc=asc)
        chartAspect.save()
        return chartAspect

    def get_svg(self, asc=0):
        params = dict()
        params['id'] = '%s_%s_aspect' % (self.p1.planet.code, self.p2.planet.code)
        params['x1'] = self.p1.get_x_aspect()
        params['y1'] = self.p1.get_y_aspect()
        params['x2'] = self.p2.get_x_aspect()
        params['y2'] = self.p2.get_y_aspect()

        color = 'black'
        if self.exact == 60 or self.exact==120:
            color = 'blue'
        if self.exact == 90 or self.exact == 180:
            color = 'red'

        params['color'] = color



        svg = '<svg class="svg_aspect"><line id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{color};stroke-width:1"></line></svg>'.format(**params)
        return svg




class Chart(models.Model):

    N_PLANETS = swe.NPLANETS
    user = models.ForeignKey(UserProfile, related_name='charts')
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

    planet_positions = models.ManyToManyField(Planet, through=PlanetPosition)
    planets_in_signs = models.ManyToManyField(PlanetInSign)
    planets_in_houses = models.ManyToManyField(PlanetInHouse)
    houses_in_signs = models.ManyToManyField(HouseInSign)
    aspects = models.ManyToManyField(Aspect, through=ChartAspect)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def create(cls, user, name, date, time=None, city=None):
        chart = Chart(user=user, name=name, date=date, time=time, city=city)
        chart.save()
        return chart

    def save(self, *args, **kwargs):
        planet_angles, planet_speeds, house_angles = self.calculate()
        super(Chart, self).save()
        self.create_relations(planet_angles, planet_speeds, house_angles)

    def create_relations(self, planet_angles, planet_speeds, house_angles):
        self.create_planet_in_signs(planet_angles)
        self.create_planet_positions(planet_angles, planet_speeds, house_angles)
        if house_angles:
            self.create_houses_in_signs(house_angles)
            self.create_planets_in_houses(planet_angles, house_angles)

    def julday(self, d):
        j = swe.julday(d.year, d.month, d.day, d.hour + d.minute/60.0)
        return j

    def swe_calc(self):
        datetime_utc = self.datetime.astimezone(pytz.utc)
        j = self.julday(datetime_utc)
        swe_calcs = [swe.calc_ut(j, i) for i in range(Chart.N_PLANETS)]
        planet_angles = [i[0] for i in swe_calcs]
        planet_speeds = [i[3] for i in swe_calcs]
        house_angles = None
        if self.lat and self.lng:
            house_angles = swe.houses(j, self.lat, self.lng)[0]

        return planet_angles, planet_speeds, house_angles


    def update_datetime_city(self):
        if self.time:
            self.datetime = datetime.combine(self.date, self.time)
        else:
            self.datetime = datetime.combine(self.date, time(12, 0))

        if self.city:
            self.datetime = self.city.timezone.localize(self.datetime)
            self.city_name = self.city.name
            self.lat = self.city.lat
            self.lng = self.city.lng
        else:
            self.datetime = pytz.utc.localize(self.datetime)

    def calculate(self):
        self.update_datetime_city()

        planet_angles, planet_speeds, house_angles = self.swe_calc()
        for planet in Planet.objects.all():
            angle = planet_angles[planet.index]
            setattr(self, planet.code, angle)
        if house_angles:
            for house in House.objects.all():
                angle = house_angles[house.index]
                setattr(self, house.code, angle)
        return planet_angles, planet_speeds, house_angles


    def create_planet_positions(self, planet_angles, planet_speeds, house_angles):
        positions = []
        for planet in Planet.objects.all():
            angle = planet_angles[planet.index]
            speed = planet_speeds[planet.index]
            sign = Sign.objects.get(index=angle/30)


            existent_position = PlanetPosition.objects.filter(chart=self, planet=planet)
            if existent_position:
                position = existent_position[0]
            else:
                position = PlanetPosition()

            if house_angles:
                position.asc = house_angles[0]
                for i in range(len(house_angles)):
                    if house_angles[i] <= angle < house_angles[(i+1) % len(house_angles)]:
                        house = House.objects.get(index=i)
                        position.house = house
                        planet_in_house = PlanetInHouse.objects.get(planet=planet, house=house)
                        position.planet_in_house = planet_in_house
                        break
            planet_in_sign = PlanetInSign.objects.get(planet=planet, sign=sign)


            position.chart = self
            position.planet = planet
            position.sign = sign

            position.angle = angle
            position.speed = speed
            position.planet_in_sign = planet_in_sign

            position.save()
            positions.append(position)

        asc = 0
        if house_angles:
            asc = house_angles[0]
        for i, a1 in enumerate(positions):
            for j, a2 in enumerate(positions):
                if i < j:
                    ChartAspect.create(self, i, j, a1, a2, asc=asc)


    def create_planet_in_signs(self, planet_angles):
        signs = {s.index: s for s in Sign.objects.all()}


        for planet in Planet.objects.all():
            angle = planet_angles[planet.index]
            sign = signs[int(angle/30)]
            p = self.planets_in_signs.filter(planet=planet)
            if p:
                p = p[0]
                if p.sign != sign:
                    self.planets_in_signs.remove(p)
                else:
                    continue
            self.planets_in_signs.add(PlanetInSign.objects.get(planet=planet, sign=sign))

    def create_houses_in_signs(self, house_angles):
        signs = {s.index: s for s in Sign.objects.all()}
        for house in House.objects.all():
            angle = house_angles[house.index]
            sign = signs[int(angle/30)]
            p = self.houses_in_signs.filter(house=house)
            if p:
                p = p[0]
                if p.sign != sign:
                    self.houses_in_signs.remove(p)
                else:
                    continue
            self.houses_in_signs.add(HouseInSign.objects.get(house=house, sign=sign))

    def create_planets_in_houses(self, planet_angles, house_angles):
        for planet in Planet.objects.all():
            angle = planet_angles[planet.index]
            for i in range(len(house_angles)):
                if house_angles[i] <= angle < house_angles[(i+1) % len(house_angles)]:
                    house = House.objects.get(index=i)
                    break
            p = self.planets_in_houses.filter(planet=planet)
            if p:
                p = p[0]
                if p.house != house:
                    self.planets_in_houses.remove(p)
                else:
                    continue
            self.planets_in_houses.add(PlanetInHouse.objects.get(planet=planet, house=house))






#@receiver(pre_delete, sender=Chart)
#def delete_repo(sender, instance, **kwargs):
#./m    instance.planet_positions.all().delete()