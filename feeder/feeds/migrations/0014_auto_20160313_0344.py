# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0013_auto_20160311_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
