#coding: utf-8
from django import template
from django.templatetags.static import static
register = template.Library()


@register.filter
def dms(value):
    """Degrees minutes seconds"""
    mnt, sec = divmod(value*3600, 60)
    deg, mnt = divmod(mnt, 60)
    deg, mnt, sec = int(deg), int(mnt), int(sec)
    return u"%s° %s' %s\"" % (deg, mnt, sec)

SIGN_SVG = ['01-aries.svg',
 '02-taurus.svg',
 '03-gemini.svg',
 '04-cancer.svg',
 '05-leo.svg',
 '06-virgo.svg',
 '07-libra.svg',
 '08-scorpio.svg',
 '09-sagittarius.svg',
 '10-capricorn.svg',
 '11-aquarius.svg',
 '12-pisces.svg']

@register.filter
def sign_img(value):
    r = ''
    if value and value>=0:
        i = int(value/30)
        r = static('clevenus/signs/'+SIGN_SVG[i])
    else:
        r = static('clevenus/signs/00-unknown.svg')


    return r

