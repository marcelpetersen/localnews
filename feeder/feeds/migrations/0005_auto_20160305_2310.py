# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0004_exclude_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exclude',
            name='source',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
