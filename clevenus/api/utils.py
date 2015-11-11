#coding: utf-8
from datetime import datetime, timedelta
import swisseph as swe
import json


cnj = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Conjunction-symbol.svg/32px-Conjunction-symbol.svg.png"
opp = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Opposition-symbol.svg/32px-Opposition-symbol.svg.png"
tri = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Trine-symbol.svg/32px-Trine-symbol.svg.png"
sqr = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Square-symbol.svg/32px-Square-symbol.svg.png"
sxt = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Sextile-symbol.svg/32px-Sextile-symbol.svg.png"

venus="https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Venus_symbol.svg/32px-Venus_symbol.svg.png"
jupiter = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Jupiter_symbol.svg/32px-Jupiter_symbol.svg.png"

ORB = 5


def boundaries_generator(predicate, iterable):
    iterable = iter(iterable)
    while True:
        finished = False
        for x in iterable:
            if predicate(x):
                finished = True
                yield x
                break
        for x in iterable:
            if not predicate(x):
                finished = True
                yield x
                break
        if not finished:
            break
        
        

def boundaries(predicate, iterable, fillvalue=None):
    from itertools import zip_longest
    gen = list(boundaries_generator(predicate, iterable))
    even = gen[::2]
    odd = gen[1::2]
    
    return list(zip_longest(even,odd,fillvalue=fillvalue))
    
class AspectType(object):
    def __init__(self, name, angle, url):
        self.name = name
        self.angle = angle
        self.url = url

ASPECTS = [
    AspectType(angle=0, name='Conjunction', url=cnj),
    AspectType(angle=60, name='Sextile', url=sxt),
    AspectType(angle=90, name='Square', url=sqr),
    AspectType(angle=120, name='Trine', url=tri),
    AspectType(angle=180, name='Opposition', url=opp),
]

ASPECTS_TYPES = {
    0: AspectType(angle=0, name='Conjunction', url=cnj),
    60: AspectType(angle=60, name='Sextile', url=sxt),
    90: AspectType(angle=90, name='Square', url=sqr),
    120: AspectType(angle=120, name='Trine', url=tri),
    180: AspectType(angle=180, name='Opposition', url=opp),

}

class Aspect(object):
    def __init__(self, date):
        self.date = date.strftime("%Y-%m-%d %H:%M")
        self.aspects = []


def julday(date):
    return swe.julday(date.year, date.month, date.day, date.hour + date.minute/60.0)

def diff(a1, a2):
    return min(abs(a1-a2), abs(360 - abs(a1-a2)))

def dms(angle):
    d = int(angle)
    m = int((angle - d) * 60)
    s = int((angle - d - m/60.0)*3600)
    return u"%d° %d\'" % (d, m)

def pos(date, p_index):
    
    x, y, z, dx, dy, dz = swe.calc(julday(date), p_index)
    return x, dx


class NewAspect(object):
    def __init__(self, aspect, value):
        self.aspect = aspect
        self.name = aspect.name
        self.url = aspect.url
        self.value = value
        self.percent = int(100.0*value/ORB)
    
class AspectCalculator(object):
    def __init__(self, date, p1, p2):
        self.date = date
        self.date_str = date.strftime("%Y-%m-%d %H:%M")
        self.a1, self.dx1 = pos(date, p1)
        self.a2, self.dx2 = pos(date, p2)
        self.diff = diff(self.a1, self.a2)
        self.calc()
        self.aspect = self.gen_aspect()
    
    def __repr__(self):
        return "<%s %d %.2f (%.2f) (%.2f) [%.2f]>" % (self.date, self.exact, self.orb, self.a1, self.a2, self.diff)    
    
    def calc(self):
        a, b = divmod(self.diff, 30)
        c, d = map(abs, divmod(self.diff, -30))
        orb, exact = min( (b, a), (d, c))
        exact *= 30
        self.orb = orb
        self.dms = dms(orb)
        self.exact = int(exact)
    
    def gen_aspect(self):
        if self.more_close_orb():
            aspect = ASPECTS_TYPES[self.exact]
            value = max(ORB-self.orb, 0)
            return NewAspect(aspect, value)
    
    def more_close_orb(self):
        if self.close_orb() and self.orb <ORB:
            return True
        return False
            
    
    def close_orb(self):
        if self.exact in [0, 60, 90, 120, 180]:
            if self.orb < ORB*4:
                return True
        return False


def gen_data(p1_index, p2_index, rev):
    today = datetime.today().replace(hour=12, minute=0, second=0, microsecond=0)
    base = today - timedelta(days=rev)
    final_date = today + timedelta(days=rev*2)
    date = base
    points = []

    if rev<50:
        big_delta = timedelta(hours=6)
        small_delta = timedelta(hours=1)
    elif rev < 700:
        big_delta = timedelta(days=1)
        small_delta = timedelta(hours=6)
    else:
        big_delta = timedelta(days=30)
        small_delta = timedelta(days=1)

    while date <= final_date:
        a = AspectCalculator(date, p1_index, p2_index)
        points.append(a)
        if a.close_orb():
            date += small_delta
        else:
            date += big_delta
            #date = date.replace(hour=12)            
    return points
    
def gen_dict(p1, p2, rev):
    raw_data = gen_data(p1.index, p2.index, rev)
    data = []
    for i in raw_data:
        
        d = {
            'date': str(i.date),
            'date_str': str(i.date_str),            
            'dms': i.dms,            
            "url": "#raptors",
        }
        if i.aspect:
            d[i.aspect.name] = i.aspect.percent
            d["percent"]= i.aspect.percent,
        data.append(d)
        
    retro = []
    for date, to_date in boundaries(lambda x:x.dx1<0, raw_data, raw_data[-1]):
        retro.append({
            'date': date.date_str,
            'toDate': to_date.date_str,
            'label': p1.name
        })

    for date, to_date in boundaries(lambda x:x.dx2<0, raw_data, raw_data[-1]):
        retro.append({
            'date': date.date_str,
            'toDate': to_date.date_str,
            'label': "%s retrograde" % p2.name
        })
    result = {
        'p1': p1.name,
        'p2': p2.name,
        'data': data,
        'retro': retro,
    }
    return result