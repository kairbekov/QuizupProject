# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20150710_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id_1', models.IntegerField()),
                ('user_id_2', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_id_1', models.IntegerField()),
                ('question_id_2', models.IntegerField()),
                ('question_id_3', models.IntegerField()),
                ('question_id_4', models.IntegerField()),
                ('question_id_5', models.IntegerField()),
                ('user1_answer_1', models.CharField(max_length=256)),
                ('user1_answer_2', models.CharField(max_length=256)),
                ('user1_answer_3', models.CharField(max_length=256)),
                ('user1_answer_4', models.CharField(max_length=256)),
                ('user1_answer_5', models.CharField(max_length=256)),
                ('user2_answer_1', models.CharField(max_length=256)),
                ('user2_answer_2', models.CharField(max_length=256)),
                ('user2_answer_3', models.CharField(max_length=256)),
                ('user2_answer_4', models.CharField(max_length=256)),
                ('user2_answer_5', models.CharField(max_length=256)),
                ('point1_1', models.IntegerField()),
                ('point1_2', models.IntegerField()),
                ('point1_3', models.IntegerField()),
                ('point1_4', models.IntegerField()),
                ('point1_5', models.IntegerField()),
                ('point2_1', models.IntegerField()),
                ('point2_2', models.IntegerField()),
                ('point2_3', models.IntegerField()),
                ('point2_4', models.IntegerField()),
                ('point2_5', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id_1', models.IntegerField()),
                ('user_id_2', models.IntegerField()),
                ('game_id', models.IntegerField()),
                ('category_id', models.CharField(max_length=256)),
                ('game_status', models.CharField(max_length=256)),
                ('point_1', models.CharField(max_length=256)),
                ('point_2', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
