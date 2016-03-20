# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0017_states'),
    ]

    operations = [
        migrations.AddField(
            model_name='states',
            name='city',
            field=models.CharField(default='Tulsa, OK, USA', max_length=200),
            preserve_default=False,
        ),
    ]
