# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_pool_rank2_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pool',
            name='rank2_id',
        ),
        migrations.RemoveField(
            model_name='pool',
            name='user2_id',
        ),
        migrations.AddField(
            model_name='categories',
            name='subcategory',
            field=models.CharField(default='subcat', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questions',
            name='level',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
