# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0020_auto_20160320_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeds',
            name='image',
            field=models.URLField(max_length=400),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='link',
            field=models.URLField(max_length=400),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='source',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='title',
            field=models.CharField(unique=True, max_length=400),
        ),
    ]
