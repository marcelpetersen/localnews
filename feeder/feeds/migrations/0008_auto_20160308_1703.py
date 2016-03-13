# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0007_auto_20160308_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exclude',
            name='user',
            field=models.ForeignKey(default=1, to='feeds.User'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(default=1, to='feeds.User'),
        ),
    ]
