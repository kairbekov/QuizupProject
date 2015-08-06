# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('subcategory', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('user1_answer_id', models.IntegerField()),
                ('user2_answer_id', models.IntegerField()),
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
                ('category_id', models.IntegerField()),
                ('game_status', models.CharField(max_length=256)),
                ('point_1', models.CharField(max_length=256)),
                ('point_2', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('rank', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('level', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('category_id', models.IntegerField()),
                ('rank', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAnswerList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_answer_1', models.CharField(max_length=256)),
                ('user_answer_2', models.CharField(max_length=256)),
                ('user_answer_3', models.CharField(max_length=256)),
                ('user_answer_4', models.CharField(max_length=256)),
                ('user_answer_5', models.CharField(max_length=256)),
                ('point_1', models.IntegerField()),
                ('point_2', models.IntegerField()),
                ('point_3', models.IntegerField()),
                ('point_4', models.IntegerField()),
                ('point_5', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
