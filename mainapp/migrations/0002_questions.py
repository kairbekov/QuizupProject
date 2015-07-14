# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_id', models.IntegerField()),
                ('question_text', models.CharField(max_length=256)),
                ('answer_1', models.CharField(max_length=256)),
                ('answer_2', models.CharField(max_length=256)),
                ('answer_3', models.CharField(max_length=256)),
                ('answer_4', models.CharField(max_length=256)),
                ('correct_answer', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
