from os.path import expanduser
activate_this_file = expanduser("~/.virtualenvs/flask/bin/activate_this.py")
execfile(activate_this_file, dict(__file__=activate_this_file))

from datetime import datetime, timedelta
import swisseph as swe

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
toolbar = DebugToolbarExtension(app)



cnj = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Conjunction-symbol.svg/32px-Conjunction-symbol.svg.png"
opp = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Opposition-symbol.svg/32px-Opposition-symbol.svg.png"
tri = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Trine-symbol.svg/32px-Trine-symbol.svg.png"
sqr = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Square-symbol.svg/32px-Square-symbol.svg.png"
sxt = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Sextile-symbol.svg/32px-Sextile-symbol.svg.png"

venus="https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Venus_symbol.svg/20px-Venus_symbol.svg.png"
jupiter = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Jupiter_symbol.svg/20px-Jupiter_symbol.svg.png"

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

class Aspect(object):
    def __init__(self, date):
        self.date = date.strftime("%Y-%m-%d %H:%M")
        self.aspects = []

class Point(object):
    def __init__(self, date, aspect_type, p1, p2):
        self.date = date
        self.aspect_type = aspect_type
        self.value = aspect(date, p1, p2, aspect_type.angle)
        self.percent = int(self.value*100)
        self.name = aspect_type.name
    
    def has_event(self):
        return self.value


def julday(date):
    return swe.julday(date.year, date.month, date.day, date.hour + date.minute/60.0)

def diff(a1, a2):
    return min(abs(a1-a2), abs(360 - (a1-a1)))

def pos(date, p_index):
    return swe.calc(julday(date), p_index)[0]

def aspect(date, p1, p2, exact=0):
    a = diff(pos(date, p1), pos(date, p2))
    return max(2 - abs(a-exact), 0)

def gen_dates():
    base = datetime.today().replace(minute=0)
    return [base + timedelta(hours=i) for i in range(-180*24, 540*24)]

def gen_data():
    aspects = {}
    dates = gen_dates()
    for aspect in ASPECTS:
        points = [Point(date, aspect, 3, 5) for date in dates]
        aspects[aspect] = {}
        for i, p  in enumerate(points):
            if p.has_event() or (i>0 and points[i-1].has_event()) or (i<len(points)-1 and points[i+1].has_event()):
                aspects[aspect][p.date] = p
    
    data = []
    for date in dates:
        a = Aspect(date)
        for aspect in aspects:
            if date in aspects[aspect]:
                a.aspects.append(aspects[aspect][date])
        data.append(a)
    
    return data


@app.route('/')
def view_chart():
    data = gen_data()
    today = datetime.today().date()
    return render_template('chart.html', data=data, today=today, aspects=ASPECTS, venus=venus, jupiter=jupiter)

@app.route('/test/')
def test():
    return "<html><body>Xuxu</body></html>"

if __name__ == '__main__':
    app.run(debug=True)
