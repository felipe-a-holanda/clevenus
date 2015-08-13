__author__ = 'fholanda'

from math import pi, sin, cos
import pytz
from  datetime import datetime,  time
import swisseph as swe

swe.set_ephe_path('/usr/share/libswe/ephe/')

def julday(d):
    j = swe.julday(d.year, d.month, d.day, d.hour + d.minute / 60.0)
    return j

def calc_position(d, planet_index):
    j = julday(d)
    return swe.calc_ut(j, planet_index)[0]


def default_context_processor(request):
    from astro.models import Planet, Sign
    return {'signs':Sign.objects.all(), 'planets':Planet.objects.all()}

