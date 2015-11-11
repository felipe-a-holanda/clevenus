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
           ['Sun',365.256],
           ['Moon',29.53],
           ['Mercury',87.969],
           ['Venus',224.701],
           ['Mars',686.98],
           ['Jupiter',11.862*365.256],
           ['Saturn',29.457*365.256],
           ['Uranus',84.011*365.256],
           ['Neptune',164.79*365.256],
           ['Pluto',247.68*365.256],
           ['Mean_Node',0],
           ['True_Node',0],
           ['Mean_Apog',0],
           ['Oscu_Apog',0],
           ['Earth',0],
           ['Chiron',0],
           ['Pholus',0],
           ['Ceres',4.599*365.2560],
           ['Pallas',0],
           ['Juno',0],
           ['Vesta',0],
           ['Intp_Apog',0],
           ['Intp_Perg',0],
           ]

HOUSES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']

ASPECT_TYPES = [('con', 'Conjunction', 0, 'conjunct'),
             ('sxt', 'Sextile', 60, 'sextile'),
             ('sqr', 'Square', 90, 'square'),
             ('tri', 'Trine', 120, 'trine'),
             ('opp', 'Opposition', 180, 'opposite'),
             ]

def orb(p1, p2, aspect):
    if p1.index >= 10 or p2.index >= 10:
        return 0
    if aspect == 60:
        return 6
    return 10



class Command(BaseCommand):
    help = 'Populate initial astro data'

    def create_signs(self):
        print('create_signs')
        for i, name in enumerate(SIGNS):
            o, _ = Sign.objects.get_or_create(name=name, code=name.lower(), index=i)
            o.save()
            print(' ', o)

    def create_planets(self):
        print('create_planets')
        for i, p in enumerate(PLANETS):
            name, rev = p
            o, _ = Planet.objects.get_or_create(name=name, code=name.lower(), index=i, revolution=rev)
            o.save()
            print(' ', o)

    def create_houses(self):
        print('create_houses')
        for i, name in enumerate(HOUSES):
            o, _ = House.objects.get_or_create(name=name, code='house_%d' %(i+1), index=i)
            o.save()
            print(' ', o)

    def create_planets_in_signs(self):
        print('create_planets_in_signs')
        planets = Planet.objects.all()
        signs = Sign.objects.all()

        for p in planets:
            for s in signs:
                o, _ = PlanetInSign.objects.get_or_create(planet=p, sign=s)
                o.save()
                print(' ', o)

    def create_planets_in_houses(self):
        print('create_planets_in_houses')
        planets = Planet.objects.all()
        houses = House.objects.all()

        for p in planets:
            for h in houses:
                o, _ = PlanetInHouse.objects.get_or_create(planet=p, house=h)
                o.save()
                print(' ', o)

    def create_houses_in_signs(self):
        print('create_houses_in_signs')
        houses = House.objects.all()
        signs = Sign.objects.all()

        for h in houses:
            for s in signs:
                o, _ = HouseInSign.objects.get_or_create(house=h, sign=s)
                o.save()
                print(' ', o)

    def create_aspects(self):
        print('create_aspects')
        planets = Planet.objects.all()
        for p1 in planets:
            for p2 in planets:
                if p2 > p1:
                    for type in ASPECT_TYPES:
                        o, _ = Aspect.objects.get_or_create(p1=p1, p2=p2, type=type[0], orb=orb(p1, p2, type[2]))
                        o.save()
                        print(' ', o)



    @transaction.atomic
    def handle(self, *args, **options):
        self.create_signs()
        self.create_planets()
        self.create_houses()
        self.create_planets_in_signs()
        self.create_planets_in_houses()
        self.create_houses_in_signs()
        self.create_aspects()