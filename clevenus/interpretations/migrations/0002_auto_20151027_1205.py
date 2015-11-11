# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interpretations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericInterpretation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(null=True)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('obj', models.ForeignKey(to='astro.Interpretable')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InterpretationBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='interpretation',
            name='chart',
        ),
        migrations.RemoveField(
            model_name='interpretation',
            name='obj',
        ),
        migrations.RemoveField(
            model_name='interpretation',
            name='user',
        ),
        migrations.DeleteModel(
            name='Interpretation',
        ),
    ]
