# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0019_auto_20160319_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exclude',
            name='source',
            field=models.CharField(max_length=255),
        ),
    ]
