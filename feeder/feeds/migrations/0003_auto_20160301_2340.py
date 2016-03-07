# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_auto_20160301_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeds',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
