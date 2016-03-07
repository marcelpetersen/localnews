# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feeds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=255)),
                ('time', models.DateTimeField()),
                ('imageUrl', models.URLField(max_length=255)),
                ('source', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
