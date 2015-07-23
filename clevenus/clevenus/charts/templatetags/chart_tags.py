#coding: utf-8
from django import template


register = template.Library()
@register.filter
def dms(value):
    """Degrees minutes seconds"""
    mnt, sec = divmod(value*3600, 60)
    deg, mnt = divmod(mnt, 60)
    deg, mnt, sec = int(deg), int(mnt), int(sec)
    return u"%s° %s' %s\"" % (deg, mnt, sec)