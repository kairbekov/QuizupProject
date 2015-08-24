from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=256)
    subcategory = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Questions(models.Model):
    category_id = models.IntegerField()
    question_text = models.CharField(max_length=256)
    answer_1 = models.CharField(max_length=256)
    answer_2 = models.CharField(max_length=256)
    answer_3 = models.CharField(max_length=256)
    answer_4 = models.CharField(max_length=256)
    correct_answer = models.IntegerField()
    level = models.IntegerField()

class Pool(models.Model):
    category_id = models.IntegerField()
    user_id = models.IntegerField()
    rank = models.IntegerField()

class Ranking(models.Model):
    user_id = models.IntegerField()
    category_id = models.IntegerField()
    rank = models.IntegerField()

class Friends(models.Model):
    user_id_1 = models.IntegerField()
    user_id_2 = models.IntegerField()

class GameInfo(models.Model):
    user_id_1 = models.IntegerField()
    user_id_2 = models.IntegerField()
    game_id = models.IntegerField()
    category_id = models.IntegerField()
    game_status = models.IntegerField()
    point_1 = models.IntegerField()
    point_2 = models.IntegerField()
    date = models.DateTimeField()

class Game(models.Model):
    question_id_1 = models.IntegerField()
    question_id_2 = models.IntegerField()
    question_id_3 = models.IntegerField()
    question_id_4 = models.IntegerField()
    question_id_5 = models.IntegerField()
    user1_answer_id = models.IntegerField()
    user2_answer_id = models.IntegerField()


class UserAnswerList(models.Model):
    user_answer_1 = models.IntegerField()
    user_answer_2 = models.IntegerField()
    user_answer_3 = models.IntegerField()
    user_answer_4 = models.IntegerField()
    user_answer_5 = models.IntegerField()
    point_1 = models.IntegerField()
    point_2 = models.IntegerField()
    point_3 = models.IntegerField()
    point_4 = models.IntegerField()
    point_5 = models.IntegerField()


