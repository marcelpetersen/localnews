# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0014_auto_20160313_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='fav_id',
            field=models.IntegerField(),
            preserve_default=False,
        ),
    ]
