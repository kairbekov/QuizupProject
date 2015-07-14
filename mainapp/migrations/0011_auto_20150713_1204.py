# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20150713_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='first_user',
            new_name='user1_answer_id',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='second_user',
            new_name='user2_answer_id',
        ),
    ]
