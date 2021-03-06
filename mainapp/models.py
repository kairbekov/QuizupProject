from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=1024)
    language = models.CharField(max_length=1024)
    def __unicode__(self):
        return self.name

class Questions(models.Model):
    category_id = models.IntegerField()
    question_text = models.CharField(max_length=1024)
    answer_1 = models.CharField(max_length=1024)
    answer_2 = models.CharField(max_length=1024)
    answer_3 = models.CharField(max_length=1024)
    answer_4 = models.CharField(max_length=1024)
    correct_answer = models.IntegerField()
    level = models.IntegerField()
    language = models.CharField(max_length=128)

class Pool(models.Model):
    category_id = models.IntegerField()
    user_id = models.IntegerField()
    rank = models.IntegerField()
    game_info_id = models.IntegerField()

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
    pts1_change = models.IntegerField()
    pts2_change = models.IntegerField()

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

class Person(models.Model):
    user_id = models.IntegerField()
    vk_id = models.BigIntegerField(null=True)
    fb_id = models.BigIntegerField(null=True)
    city = models.CharField(max_length=1024, null=True)
    avatar = models.CharField(max_length=1024, null=True)
    total_points = models.IntegerField()
    reg_id = models.CharField(max_length=1024, null=True)

class Invitation(models.Model):
    game_id = models.IntegerField()
    challenger_id = models.IntegerField()
    status = models.IntegerField()

class Feedback(models.Model):
    user_id = models.IntegerField()
    text = models.TextField(null=True)
    date = models.DateField(null=True)


class SiteMessages(models.Model):
    username = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    topic = models.CharField(max_length=256)
    message = models.TextField()
    date = models.DateField(null=True)