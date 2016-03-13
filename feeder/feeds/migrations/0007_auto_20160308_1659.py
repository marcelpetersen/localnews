# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_auto_20160308_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='exclude',
            name='user',
            field=models.ForeignKey(default=1, to='feeds.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(default=1, to='feeds.User'),
            preserve_default=False,
        ),
    ]
