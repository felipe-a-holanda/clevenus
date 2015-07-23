from django.contrib import admin

# Register your models here.
from .models import *


class Interpretabledmin(admin.ModelAdmin):
    ordering = ['type', 'iname']


class SignAdmin(admin.ModelAdmin):
    exclude = ['iname']
    ordering = ['index']


class PlanetAdmin(admin.ModelAdmin):
    exclude = ['iname']
    ordering = ['index']


class HouseAdmin(admin.ModelAdmin):
    exclude = ['iname']
    ordering = ['index']

class PlanetInSignAdmin(admin.ModelAdmin):
    exclude = ['iname']
    ordering = ['planet', 'sign']

class PlanetInHouseAdmin(admin.ModelAdmin):
    exclude = ['iname']
    ordering = ['planet', 'house']

class HouseInSignAdmin(admin.ModelAdmin):
    exclude = ['iname']
    ordering = ['house', 'sign']

class AspectAdmin(admin.ModelAdmin):
    exclude = ['iname']
    ordering = ['p1', 'p2', 'degrees']

admin.site.register(Sign, SignAdmin)
admin.site.register(Planet, PlanetAdmin)
admin.site.register(House, HouseAdmin)

admin.site.register(PlanetInSign, PlanetInSignAdmin)
admin.site.register(PlanetInHouse, PlanetInHouseAdmin)
admin.site.register(HouseInSign, HouseInSignAdmin)

admin.site.register(Aspect, AspectAdmin)
