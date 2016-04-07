# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0021_auto_20160326_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeds',
            name='image',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='link',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='source',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='title',
            field=models.TextField(unique=True),
        ),
    ]
