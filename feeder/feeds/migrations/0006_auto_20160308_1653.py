# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0005_auto_20160305_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterModelOptions(
            name='favorites',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='favorites',
            name='image',
            field=models.URLField(max_length=255, blank=True),
        ),
    ]
