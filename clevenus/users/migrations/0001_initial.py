# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True, blank=True)),
                ('datetime', models.DateTimeField(null=True)),
                ('img', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('chart', models.OneToOneField(related_name='user', null=True, to='charts.Chart')),
                ('city', models.ForeignKey(to='charts.City', null=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
