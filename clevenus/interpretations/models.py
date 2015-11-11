from django.db import models
from django.contrib.auth.models import User
from astro.models import Interpretable


class InterpretationBook(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class GenericInterpretation(models.Model):
    user = models.ForeignKey(User)
    obj = models.ForeignKey(Interpretable)
    url = models.URLField(null=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.obj)
