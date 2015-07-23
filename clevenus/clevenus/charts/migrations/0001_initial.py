# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('time', models.TimeField(null=True, blank=True)),
                ('datetime', models.DateTimeField()),
                ('city_name', models.CharField(max_length=512, null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lng', models.FloatField(null=True, blank=True)),
                ('sun', models.FloatField(verbose_name='Sun')),
                ('moon', models.FloatField(verbose_name='Moon')),
                ('mercury', models.FloatField(verbose_name='Mercury')),
                ('venus', models.FloatField(verbose_name='Venus')),
                ('mars', models.FloatField(verbose_name='Mars')),
                ('jupiter', models.FloatField(verbose_name='Jupiter')),
                ('saturn', models.FloatField(verbose_name='Saturn')),
                ('uranus', models.FloatField(verbose_name='Uranus')),
                ('neptune', models.FloatField(verbose_name='Neptune')),
                ('pluto', models.FloatField(verbose_name='Pluto')),
                ('mean_node', models.FloatField()),
                ('true_node', models.FloatField()),
                ('mean_apog', models.FloatField()),
                ('oscu_apog', models.FloatField()),
                ('earth', models.FloatField()),
                ('chiron', models.FloatField()),
                ('pholus', models.FloatField()),
                ('ceres', models.FloatField()),
                ('pallas', models.FloatField()),
                ('juno', models.FloatField()),
                ('vesta', models.FloatField()),
                ('intp_apog', models.FloatField()),
                ('intp_perg', models.FloatField()),
                ('house_1', models.FloatField(null=True, blank=True)),
                ('house_2', models.FloatField(null=True, blank=True)),
                ('house_3', models.FloatField(null=True, blank=True)),
                ('house_4', models.FloatField(null=True, blank=True)),
                ('house_5', models.FloatField(null=True, blank=True)),
                ('house_6', models.FloatField(null=True, blank=True)),
                ('house_7', models.FloatField(null=True, blank=True)),
                ('house_8', models.FloatField(null=True, blank=True)),
                ('house_9', models.FloatField(null=True, blank=True)),
                ('house_10', models.FloatField(null=True, blank=True)),
                ('house_11', models.FloatField(null=True, blank=True)),
                ('house_12', models.FloatField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChartAspect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('angle', models.FloatField()),
                ('exact', models.FloatField()),
                ('diff', models.FloatField()),
                ('asc', models.FloatField(default=0)),
                ('aspect', models.ForeignKey(to='astro.Aspect')),
                ('chart', models.ForeignKey(to='charts.Chart')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('city', models.CharField(max_length=512)),
                ('state', models.CharField(max_length=512)),
                ('country', models.CharField(max_length=512)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('timezone', timezone_field.fields.TimeZoneField()),
            ],
        ),
        migrations.CreateModel(
            name='PlanetPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('asc', models.FloatField(default=0)),
                ('angle', models.FloatField()),
                ('speed', models.FloatField()),
                ('chart', models.ForeignKey(to='charts.Chart')),
                ('house', models.ForeignKey(blank=True, to='astro.House', null=True)),
                ('planet', models.ForeignKey(to='astro.Planet')),
                ('planet_in_house', models.ForeignKey(blank=True, to='astro.PlanetInHouse', null=True)),
                ('planet_in_sign', models.ForeignKey(to='astro.PlanetInSign')),
                ('sign', models.ForeignKey(to='astro.Sign')),
            ],
        ),
        migrations.AddField(
            model_name='chartaspect',
            name='p1',
            field=models.ForeignKey(related_name='chart_aspects_first', verbose_name=b'First Planet', to='charts.PlanetPosition'),
        ),
        migrations.AddField(
            model_name='chartaspect',
            name='p2',
            field=models.ForeignKey(related_name='chart_aspects_second', verbose_name=b'Second Planet', to='charts.PlanetPosition'),
        ),
        migrations.AddField(
            model_name='chart',
            name='aspects',
            field=models.ManyToManyField(to='astro.Aspect', through='charts.ChartAspect'),
        ),
        migrations.AddField(
            model_name='chart',
            name='city',
            field=models.ForeignKey(blank=True, to='charts.City', null=True),
        ),
        migrations.AddField(
            model_name='chart',
            name='houses_in_signs',
            field=models.ManyToManyField(to='astro.HouseInSign'),
        ),
        migrations.AddField(
            model_name='chart',
            name='planet_positions',
            field=models.ManyToManyField(to='astro.Planet', through='charts.PlanetPosition'),
        ),
        migrations.AddField(
            model_name='chart',
            name='planets_in_houses',
            field=models.ManyToManyField(to='astro.PlanetInHouse'),
        ),
        migrations.AddField(
            model_name='chart',
            name='planets_in_signs',
            field=models.ManyToManyField(to='astro.PlanetInSign'),
        ),
    ]
