# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feeds', '0018_states_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('link', models.CharField(max_length=255, blank=True)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('user', models.ForeignKey(related_name='suggester', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AlterModelOptions(
            name='states',
            options={'ordering': ['-id']},
        ),
    ]
