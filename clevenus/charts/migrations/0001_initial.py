# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True)),
                ('datetime', models.DateTimeField()),
                ('city_name', models.CharField(blank=True, max_length=512, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
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
                ('house_1', models.FloatField(blank=True, null=True)),
                ('house_2', models.FloatField(blank=True, null=True)),
                ('house_3', models.FloatField(blank=True, null=True)),
                ('house_4', models.FloatField(blank=True, null=True)),
                ('house_5', models.FloatField(blank=True, null=True)),
                ('house_6', models.FloatField(blank=True, null=True)),
                ('house_7', models.FloatField(blank=True, null=True)),
                ('house_8', models.FloatField(blank=True, null=True)),
                ('house_9', models.FloatField(blank=True, null=True)),
                ('house_10', models.FloatField(blank=True, null=True)),
                ('house_11', models.FloatField(blank=True, null=True)),
                ('house_12', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChartAspect',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('angle', models.FloatField()),
                ('exact', models.FloatField()),
                ('diff', models.FloatField()),
                ('aspect', models.ForeignKey(related_name='chart_aspects', to='astro.Aspect')),
                ('chart', models.ForeignKey(to='charts.Chart')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=512)),
                ('city', models.CharField(max_length=512)),
                ('state', models.CharField(max_length=512)),
                ('country', models.CharField(max_length=512)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('timezone', timezone_field.fields.TimeZoneField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=512)),
                ('datetime', models.DateTimeField()),
                ('known_time', models.BooleanField()),
                ('chart', models.ForeignKey(to='charts.Chart', null=True)),
                ('city', models.ForeignKey(to='charts.City')),
            ],
        ),
        migrations.AddField(
            model_name='chart',
            name='aspects',
            field=models.ManyToManyField(through='charts.ChartAspect', related_name='charts', to='astro.Aspect'),
        ),
        migrations.AddField(
            model_name='chart',
            name='city',
            field=models.ForeignKey(blank=True, null=True, to='charts.City'),
        ),
        migrations.AddField(
            model_name='chart',
            name='houses_in_signs',
            field=models.ManyToManyField(related_name='charts', to='astro.HouseInSign'),
        ),
        migrations.AddField(
            model_name='chart',
            name='planets_in_houses',
            field=models.ManyToManyField(related_name='charts', to='astro.PlanetInHouse'),
        ),
        migrations.AddField(
            model_name='chart',
            name='planets_in_signs',
            field=models.ManyToManyField(related_name='charts', to='astro.PlanetInSign'),
        ),
    ]
