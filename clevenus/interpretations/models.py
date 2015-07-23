from django.db import models
from django.contrib.auth.models import User

from charts.models import Chart
from astro.models import Interpretable




class Interpretation(models.Model):
    user = models.ForeignKey(User)
    chart = models.ForeignKey(Chart, blank=True, null=True)
    obj = models.ForeignKey(Interpretable)

    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)