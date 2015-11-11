from django.db import models
from django.utils.text import slugify
# Create your models here.
from django.core.urlresolvers import reverse
from django.templatetags.static import static
from .utils import calc_position
from datetime import datetime, timedelta


class Interpretable(models.Model):
    iname = models.CharField(max_length=20, unique=True)

    @property
    def url(self):
        return self.get_absolute_url()

    def __str__(self):
        return self.iname


class Sign(Interpretable):
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20, unique=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('sign-view', args=[str(self.slug)])

    @property
    def start_angle(self):
        return self.index*30

    @property
    def end_angle(self):
        return (self.index+1)*30

    def __str__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.index, other.index)

    def __lt__(self, other):
        return self.index < other.index

    def save(self, *args, **kwargs):
        self.iname = self.name
        self.slug = slugify(self.code)
        super(Sign, self).save(*args, **kwargs)


class Planet(Interpretable):
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20, unique=True)
    slug = models.SlugField()
    revolution = models.FloatField()

    def get_absolute_url(self):
        return reverse('planet-view', args=[str(self.slug)])


    def img(self):
        return static('clevenus/planets/%02d-%s.svg' % (self.index+1, self.code))


    def __str__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.index, other.index)

    def __lt__(self, other):
        return self.index < other.index

    def save(self, *args, **kwargs):
        self.iname = self.name
        self.slug = slugify(self.name)
        super(Planet, self).save(*args, **kwargs)

    def get_positions(self):
        from charts.utils import CONSTS
        base = datetime.today()
        date_list = [base + timedelta(days=x) for x in range(-180, 365)]
        positions = []
        for date in date_list:
            angle = calc_position(date, self.index)
            sign = CONSTS.signs[int(angle/30)]
            d = {'date':date, 'angle':angle, 'sign':sign}
            positions.append(d)

        return positions



class House(Interpretable):
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20, unique=True)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('house-view', args=[str(self.slug)])


    def __str__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.index, other.index)

    def __lt__(self, other):
        return self.index < other.index

    def save(self, *args, **kwargs):
        self.iname = self.name
        self.slug = slugify(self.code)
        super(House, self).save(*args, **kwargs)


class PlanetInSign(Interpretable):
    name = models.CharField(max_length=40, unique=True)
    planet = models.ForeignKey(Planet)
    sign = models.ForeignKey(Sign)
    code = models.CharField(max_length=40, unique=True)
    slug = models.SlugField()
    planet_slug = models.SlugField()
    sign_slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('planet-in-sign', args=[self.planet_slug, self.sign_slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "%s in %s" % (self.planet.name, self.sign.name)
        self.iname = self.name
        self.slug = slugify(self.name)
        self.planet_slug = self.planet.slug
        self.sign_slug = self.sign.slug
        self.code = self.slug
        super(PlanetInSign, self).save(*args, **kwargs)

class HouseInSign(Interpretable):
    name = models.CharField(max_length=40, unique=True)
    house = models.ForeignKey(House)
    sign = models.ForeignKey(Sign)
    slug = models.SlugField()
    house_slug = models.SlugField()
    sign_slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('house-in-sign', args=[self.house_slug, self.sign_slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "%s in %s" % (self.house.name, self.sign.name)
        self.iname = self.name
        self.slug = slugify(self.name)
        self.sign_slug = self.sign.slug
        self.house_slug = self.house.slug
        self.code = self.slug
        super(HouseInSign, self).save(*args, **kwargs)


class PlanetInHouse(Interpretable):
    name = models.CharField(max_length=40, unique=True)
    planet = models.ForeignKey(Planet)
    house = models.ForeignKey(House)
    slug = models.SlugField()
    planet_slug = models.SlugField()
    house_slug = models.SlugField()


    def get_absolute_url(self):
        return reverse('planet-in-house', args=[self.planet_slug, self.house_slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "%s in %s house" % (self.planet.name, self.house.name)
        self.iname = self.name
        self.slug = slugify(self.name)
        self.planet_slug = self.planet.slug
        self.house_slug = self.house.slug
        self.code = self.slug
        super(PlanetInHouse, self).save(*args, **kwargs)


class Aspect(Interpretable):
    TYPES = [('con', 'Conjunction', 0, 'conjunct'),
             ('sxt', 'Sextile', 60, 'sextile'),
             ('sqr', 'Square', 90, 'square'),
             ('tri', 'Trine', 120, 'trine'),
             ('opp', 'Opposition', 180, 'opposite'),
             ]

    name = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=3, choices=[i[:2] for i in TYPES])
    degrees = models.IntegerField()
    orb = models.FloatField(default=0)
    p1 = models.ForeignKey(Planet, verbose_name='First Planet', related_name='aspects_first')
    p2 = models.ForeignKey(Planet, verbose_name='Second Planet', related_name='aspects_second')
    slug = models.SlugField()

    p1_slug = models.SlugField()
    p2_slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('aspect', args=[self.p1_slug, self.type, self.p2_slug])

    def __str__(self):
        return self.name

    @property
    def type_verbose(self):
        return dict([(i[0], i[3]) for i in Aspect.TYPES])[self.type]

    def save(self, *args, **kwargs):
        types = {i[0]: i for i in Aspect.TYPES}
        self.name = "%s %s %s" % (self.p1.name, types[self.type][3], self.p2.name)
        self.degrees = types[self.type][2]
        self.iname = self.name
        self.slug = slugify(self.name)
        self.code = self.slug
        self.p1_slug = self.p1.slug
        self.p2_slug = self.p2.slug
        super(Aspect, self).save(*args, **kwargs)
