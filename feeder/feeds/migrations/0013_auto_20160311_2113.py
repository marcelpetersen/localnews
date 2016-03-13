# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0012_auto_20160311_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exclude',
            name='user',
            field=models.ForeignKey(related_name='exclude', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
