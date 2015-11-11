# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interpretation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('chart', models.ForeignKey(blank=True, null=True, to='charts.Chart')),
                ('obj', models.ForeignKey(to='astro.Interpretable')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
