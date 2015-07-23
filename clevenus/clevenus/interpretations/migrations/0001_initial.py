# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('astro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interpretation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('chart', models.ForeignKey(blank=True, to='charts.Chart', null=True)),
                ('obj', models.ForeignKey(to='astro.Interpretable')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
