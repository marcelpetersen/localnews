# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_auto_20160301_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exclude',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('link', models.URLField(max_length=255)),
                ('time', models.DateTimeField()),
                ('image', models.URLField(max_length=255)),
                ('source', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
