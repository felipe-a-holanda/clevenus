from django.contrib import admin

from .models import *

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



class PositionInline(admin.TabularInline):
    model = PlanetPosition
    fields = ['name',]
    readonly_fields = ['name',]


class ChartAdmin(admin.ModelAdmin):
    @classmethod
    def sign(cls, self, planet):
        angle = getattr(self, planet)
        if angle:
            return SIGNS[int(angle/30)]
        else:
            return 'Undefined'

    def ascendant(self):
        return ChartAdmin.sign(self, 'house_1')

    def sun_sign(self):
        return ChartAdmin.sign(self, 'sun')

    def moon_sign(self):
        return ChartAdmin.sign(self, 'moon')


    #inlines = (PositionInline,)
    fields = ['user', 'name', ('date', 'time'), 'city', 'house_1', 'sun', 'moon', 'planets_in_signs', 'planets_in_houses', 'houses_in_signs', 'aspects']
    list_display = ['name', 'date', 'time', 'city',  ascendant, sun_sign, moon_sign]
    readonly_fields = ['house_1', 'sun', 'moon', 'planets_in_signs', 'planets_in_houses', 'houses_in_signs', 'aspects']






class CityAdmin(admin.ModelAdmin):
    fields = ['name', 'city', 'state', 'country', ('lat', 'lng'), ]
    readonly_fields = ['city', 'state', 'country', 'lat', 'lng']
    list_display = ['city', 'state', 'country']



class ChartAspectAdmin(admin.ModelAdmin):

    list_display = ['chart', 'name', 'diff']

admin.site.register(Chart, ChartAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(PlanetPosition)
admin.site.register(ChartAspect, ChartAspectAdmin)
