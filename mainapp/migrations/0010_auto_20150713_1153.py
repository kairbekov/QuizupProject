# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_friends_game_gameinfo'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='game',
            name='point1_1',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point1_2',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point1_3',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point1_4',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point1_5',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point2_1',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point2_2',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point2_3',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point2_4',
        ),
        migrations.RemoveField(
            model_name='game',
            name='point2_5',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user1_answer_1',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user1_answer_2',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user1_answer_3',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user1_answer_4',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user1_answer_5',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user2_answer_1',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user2_answer_2',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user2_answer_3',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user2_answer_4',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user2_answer_5',
        ),
        migrations.AddField(
            model_name='game',
            name='first_user',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='second_user',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
