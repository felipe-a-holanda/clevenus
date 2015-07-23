from django.contrib import admin

# Register your models here.
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'chart', 'datetime']
    #exclude = ['iname']
    #ordering = ['p1', 'p2', 'degrees']
admin.site.register(UserProfile, UserProfileAdmin)