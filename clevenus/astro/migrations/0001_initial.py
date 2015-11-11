# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interpretable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('iname', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Aspect',
            fields=[
                ('interpretable_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('type', models.CharField(choices=[('con', 'Conjunction'), ('sxt', 'Sextile'), ('sqr', 'Square'), ('tri', 'Trine'), ('opp', 'Opposition')], max_length=3)),
                ('degrees', models.IntegerField()),
                ('orb', models.FloatField(default=0)),
                ('slug', models.SlugField()),
                ('p1_slug', models.SlugField()),
                ('p2_slug', models.SlugField()),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('interpretable_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='astro.Interpretable')),
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
                ('interpretable_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('slug', models.SlugField()),
                ('house_slug', models.SlugField()),
                ('sign_slug', models.SlugField()),
                ('house', models.ForeignKey(to='astro.House')),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('interpretable_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='astro.Interpretable')),
                ('index', models.IntegerField(unique=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('code', models.CharField(unique=True, max_length=20)),
                ('slug', models.SlugField()),
                ('revolution', models.FloatField()),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='PlanetInHouse',
            fields=[
                ('interpretable_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('slug', models.SlugField()),
                ('planet_slug', models.SlugField()),
                ('house_slug', models.SlugField()),
                ('house', models.ForeignKey(to='astro.House')),
                ('planet', models.ForeignKey(to='astro.Planet')),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='PlanetInSign',
            fields=[
                ('interpretable_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='astro.Interpretable')),
                ('name', models.CharField(unique=True, max_length=40)),
                ('code', models.CharField(unique=True, max_length=40)),
                ('slug', models.SlugField()),
                ('planet_slug', models.SlugField()),
                ('sign_slug', models.SlugField()),
                ('planet', models.ForeignKey(to='astro.Planet')),
            ],
            bases=('astro.interpretable',),
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('interpretable_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='astro.Interpretable')),
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
            field=models.ForeignKey(related_name='aspects_first', verbose_name='First Planet', to='astro.Planet'),
        ),
        migrations.AddField(
            model_name='aspect',
            name='p2',
            field=models.ForeignKey(related_name='aspects_second', verbose_name='Second Planet', to='astro.Planet'),
        ),
    ]
