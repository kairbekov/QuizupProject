# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20150612_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='user2_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ranking',
            name='rank',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
