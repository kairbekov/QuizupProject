# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20150624_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='rank2_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
