# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interpretable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iname', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Aspect',
            fields=[
                ('interpretable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('type', models.CharField(max_length=3, choices=[(b'con', b'Conjunction'), (b'sxt', b'Sextile'), (b'sqr', b'Square'), (b'tri', b'Trine'), (b'opp', b'Opposition')])),
                ('degrees', models.IntegerField()),
                ('orb', models.FloatField(default=0)),
                ('slug', models.SlugField()),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('interpretable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='astro.Interpretable')),
                ('index', models.IntegerField(unique=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('code', models.CharField(unique=True, max_length=20)),
                ('slug', models.SlugField()),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='HouseInSign',
            fields=[
                ('interpretable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('slug', models.SlugField()),
                ('house', models.ForeignKey(to='astro.House')),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('interpretable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='astro.Interpretable')),
                ('index', models.IntegerField(unique=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('code', models.CharField(unique=True, max_length=20)),
                ('slug', models.SlugField()),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='PlanetInHouse',
            fields=[
                ('interpretable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('slug', models.SlugField()),
                ('house', models.ForeignKey(to='astro.House')),
                ('planet', models.ForeignKey(to='astro.Planet')),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='PlanetInSign',
            fields=[
                ('interpretable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('code', models.CharField(unique=True, max_length=40)),
                ('slug', models.SlugField()),
                ('planet', models.ForeignKey(to='astro.Planet')),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('interpretable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='astro.Interpretable')),
                ('index', models.IntegerField(unique=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('code', models.CharField(unique=True, max_length=20)),
                ('slug', models.SlugField()),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.AddField(
            model_name='planetinsign',
            name='sign',
            field=models.ForeignKey(to='astro.Sign'),
        ),
        migrations.AddField(
            model_name='houseinsign',
            name='sign',
            field=models.ForeignKey(to='astro.Sign'),
        ),
        migrations.AddField(
            model_name='aspect',
            name='p1',
            field=models.ForeignKey(related_name='aspects_first', verbose_name=b'First Planet', to='astro.Planet'),
        ),
        migrations.AddField(
            model_name='aspect',
            name='p2',
            field=models.ForeignKey(related_name='aspects_second', verbose_name=b'Second Planet', to='astro.Planet'),
        ),
    ]
