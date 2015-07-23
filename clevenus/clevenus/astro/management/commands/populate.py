from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from astro.models import Sign, Planet, House, PlanetInSign, PlanetInHouse, HouseInSign, Aspect


SIGNS = ['Aries',
         'Taurus',
         'Gemini',
         'Cancer',
         'Leo',
         'Virgo',
         'Libra',
         'Scorpio',
         'Sagittarius',
         'Capricorn',
         'Aquarius',
         'Pisces']

PLANETS = [
           #'Ecl_Nut',
           'Sun',
           'Moon',
           'Mercury',
           'Venus',
           'Mars',
           'Jupiter',
           'Saturn',
           'Uranus',
           'Neptune',
           'Pluto',
           'Mean_Node',
           'True_Node',
           'Mean_Apog',
           'Oscu_Apog',
           'Earth',
           'Chiron',
           'Pholus',
           'Ceres',
           'Pallas',
           'Juno',
           'Vesta',
           'Intp_Apog',
           'Intp_Perg'
           ]

HOUSES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']

ASPECT_TYPES = [('con', 'Conjunction', 0, 'conjunct'),
             ('sxt', 'Sextile', 60, 'sextile'),
             ('sqr', 'Square', 90, 'square'),
             ('tri', 'Trine', 120, 'trine'),
             ('opp', 'Opposition', 180, 'opposite'),
             ]

class Command(BaseCommand):
    help = 'Populate initial astro data'

    def create_signs(self):
        print('create_signs')
        for i, name in enumerate(SIGNS):
            o, _ = Sign.objects.get_or_create(name=name, code=name.lower(), index=i)
            o.save()
            print ' ', o

    def create_planets(self):
        print('create_planets')
        for i, name in enumerate(PLANETS):
            o, _ = Planet.objects.get_or_create(name=name, code=name.lower(), index=i)
            o.save()
            print ' ', o

    def create_houses(self):
        print('create_houses')
        for i, name in enumerate(HOUSES):
            o, _ = House.objects.get_or_create(name=name, code='house_%d' %(i+1), index=i)
            o.save()
            print ' ', o

    def create_planets_in_signs(self):
        print('create_planets_in_signs')
        planets = Planet.objects.all()
        signs = Sign.objects.all()

        for p in planets:
            for s in signs:
                o, _ = PlanetInSign.objects.get_or_create(planet=p, sign=s)
                o.save()
                print ' ', o

    def create_planets_in_houses(self):
        print('create_planets_in_houses')
        planets = Planet.objects.all()
        houses = House.objects.all()

        for p in planets:
            for h in houses:
                o, _ = PlanetInHouse.objects.get_or_create(planet=p, house=h)
                o.save()
                print ' ', o

    def create_houses_in_signs(self):
        print('create_houses_in_signs')
        houses = House.objects.all()
        signs = Sign.objects.all()

        for h in houses:
            for s in signs:
                o, _ = HouseInSign.objects.get_or_create(house=h, sign=s)
                o.save()
                print ' ', o

    def create_aspects(self):
        print('create_aspects')
        planets = Planet.objects.all()
        for p1 in planets:
            for p2 in planets:
                if p2 > p1:
                    for type in ASPECT_TYPES:
                        o, _ = Aspect.objects.get_or_create(p1=p1, p2=p2, type=type[0])
                        o.save()
                        print ' ', o



    @transaction.atomic
    def handle(self, *args, **options):
        self.create_signs()
        self.create_planets()
        self.create_houses()
        self.create_planets_in_signs()
        self.create_planets_in_houses()
        self.create_houses_in_signs()
        self.create_aspects()