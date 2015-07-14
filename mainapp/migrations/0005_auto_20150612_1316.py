# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='rank',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
