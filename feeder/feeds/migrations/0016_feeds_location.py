# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0015_favorites_fav_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeds',
            name='location',
            field=models.CharField(default='OK', max_length=2),
            preserve_default=False,
        ),
    ]
