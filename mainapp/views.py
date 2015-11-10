import base64
import csv
import os
import datetime
import cStringIO
import codecs
import random
import urllib
from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.serializers import json
import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from os import path
from sets import Set
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import sys
import unicodedata
from push_notifications.models import GCMDevice
import xlrd
from mainapp.models import *
from django.db import transaction

@csrf_exempt
def login_view(request):
    results = {}
    tmp = {}
    username = request.POST['username']
    password = request.POST['password']
    tmp['success'] = False
    tmp['text'] = "Bla bla"
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            request.user = user
            login(request, user)
            tmp['success'] = True
            tmp['text'] = "Your account is ok"
            #return HttpResponse("Your account is ok.")
        else:
            tmp['success'] = True
            tmp['text'] = "Your account is disabled"
            #return HttpResponse("Your account is disabled.")
    else:
         tmp['success'] = False
         tmp['text'] = "Invalid login or password"
         #return HttpResponse("Invalid login details supplied.")
    results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def logout_view(request):
    results = {}
    tmp = {}
    tmp['success'] = True
    tmp['text'] = " "
    results['message'] = tmp
    logout(request)
    return JsonResponse(data=results)

@csrf_exempt
def registration(request):
    results = {}
    tmp = {}
    tmp['success'] = False
    tmp['text'] = "Current user is already exist"
    #username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password = request.POST['password']
    email = request.POST['email']
    if first_name and last_name and password and email:
        try:
            check = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            person = Person(user_id=user.id, vk_id=0, fb_id=0, city="Almaty", avatar="https://help.github.com/assets/images/help/profile/identicon.png", total_points=0)
            person.save()
            user = authenticate(username=email, password=password)
            login(request,user)
            for i in Categories.objects.all():
                ranking = Ranking(category_id=i.id, user_id=user.id, rank=0)
                ranking.save()
            tmp['success'] = True
            tmp['text'] = "Registred"
    else:
        tmp['text'] = "Please, set all the fields"
        tmp['success'] = False
    results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def category_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        categroy_list = []
        for i in Categories.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['category'] = i.name
            tmp['subcategory'] = i.subcategory
            categroy_list.append(tmp)
        results['message'] = categroy_list
    return JsonResponse(data=results)

@csrf_exempt
def rank_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        ranking = []
        for i in Ranking.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['category_id'] = i.category_id
            tmp['user_id'] = i.user_id
            tmp['rank'] = i.rank
            ranking.append(tmp)
        results['message'] = ranking
    return JsonResponse(data=results)

@csrf_exempt
def friend_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        friends = []
        for i in Friends.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['user_id_1'] = i.user_id_1
            tmp['user_id_2'] = i.user_id_2
            friends.append(tmp)
        results['message'] = friends
    return JsonResponse(data=results)

@csrf_exempt
def get_my_profile(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        profile = {}
        tmp = User.objects.get(id=request.user.id)
        person = Person.objects.get(user_id=tmp.id)
        profile['success'] = True
        profile['text'] = "Your profile"
        profile['id'] = tmp.id
        profile['first_name'] = tmp.first_name
        profile['last_name'] = tmp.last_name
        profile['avatar'] = convertImgToString(person.avatar)
        profile['total_points'] = person.total_points
        results['message'] = profile
    return JsonResponse(data=results)

@csrf_exempt
def get_my_category_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        category_list = []
        listOfId = []
        for i in GameInfo.objects.filter(Q(user_id_1 = request.user.id) | Q(user_id_2 = request.user.id)):
            listOfId.append(i.category_id)
        listOfId = set(listOfId)
        listOfId = list(listOfId)
        for i in listOfId:
            tmp = {}
            k = Categories.objects.get(id=i)
            tmp['id'] = k.id
            tmp['name'] = k.name
            tmp['subcategory'] = k.subcategory
            category_list.append(tmp)
        results['message'] = category_list
    return JsonResponse(data=results)

@csrf_exempt
def get_my_rank_by_category(request):
    results = {}
    error = {}
    category_id = request.POST['id']
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        ranking = {}
        tmp = Ranking.objects.get(user_id=request.user.id, category_id=category_id)
        ranking['success'] = True
        ranking['text'] = "My rank by category"
        ranking['category_name'] = Categories.objects.get(id=tmp.category_id).name
        ranking['category_point'] = tmp.rank
        ranking['category_id'] = Categories.objects.get(id=tmp.category_id).id
        results['message'] = ranking
    return JsonResponse(data=results)

# Win = 1
# Draw = 0
# Lose = -1
@csrf_exempt
def get_played_games_list(request):
    results = {}
    list = []
    error = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        for i in GameInfo.objects.filter((Q(user_id_1=request.user.id) | Q(user_id_2=request.user.id)) & Q(game_status=4)).order_by('-date'):
            opponent = User.objects.get(id=i.user_id_1)
            if i.user_id_1 == request.user.id:
                opponent = User.objects.get(id=i.user_id_2)
            games_list = {}
            games_list['opponent_name'] = opponent.first_name
            games_list['avatar'] = convertImgToString(Person.objects.get(user_id=opponent.id).avatar)
            games_list['date'] = (i.date).strftime("%Y-%m-%d %H:%M")
            status = " "
            if (request.user.id == i.user_id_1 and int(i.point_1) > int(i.point_2)) or (request.user.id == i.user_id_2 and int(i.point_1) < int(i.point_2)):
                status = 1
            elif (request.user.id == i.user_id_1 and int(i.point_1) < int(i.point_2)) or (request.user.id == i.user_id_2 and int(i.point_1) > int(i.point_2)):
                status = -1
            else:
                status = 0
            games_list['status'] = status
            games_list['category_name'] = Categories.objects.get(id=i.category_id).name
            games_list['game_id'] = i.game_id
            list.append(games_list)
        results['message'] = list
        if len(list) == 0:
            results['Message'] = "No any games!"
    return JsonResponse(data=results)

@csrf_exempt
def get_played_game_info(request):
    results = {}
    list = []
    error = {}
    game_info_id = request.POST['id']
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        gameInfo = GameInfo.objects.get(id=game_info_id)
        game = Game.objects.get(id=gameInfo.game_id)
        user1 = UserAnswerList.objects.get(id=game.user1_answer_id)
        user2 = UserAnswerList.objects.get(id=game.user2_answer_id)
        questions = []
        questions.append(Questions.objects.get(id=game.question_id_1))
        questions.append(Questions.objects.get(id=game.question_id_2))
        questions.append(Questions.objects.get(id=game.question_id_3))
        questions.append(Questions.objects.get(id=game.question_id_4))
        questions.append(Questions.objects.get(id=game.question_id_5))
        for i in range(0,5):
            tmp = {}
            tmp['number'] = i+1
            tmp['question'] = questions[i].question_text
            tmp['answer_1'] = questions[i].answer_1
            tmp['answer_2'] = questions[i].answer_2
            tmp['answer_3'] = questions[i].answer_3
            tmp['answer_4'] = questions[i].answer_4
            tmp['right_answer'] = questions[i].correct_answer
            tmp['user1_answer'] = user1.user_answer_1
            tmp['user1_point'] = user1.point_1
            tmp['user2_answer'] = user2.user_answer_1
            tmp['user2_point'] = user2.point_1
            list.append(tmp)
        results['message'] = list
    return JsonResponse(data=results)

def generateQuestions(category_id):
    list = []
    sample = []
    try:
        for i in Questions.objects.all():
            if i.category_id == category_id:
                sample.append(i)
    except Questions.DoesNotExist:
        pass
    p = random.sample(sample, 5)
    for i in p:
        tmp = {}
        tmp['id'] = i.id
        tmp['question'] = i.question_text
        tmp['answer_1'] = i.answer_1
        tmp['answer_2'] = i.answer_2
        tmp['answer_3'] = i.answer_3
        tmp['answer_4'] = i.answer_4
        tmp['correct_answer'] = i.correct_answer
        list.append(tmp)
        print tmp
    return list

@csrf_exempt
def get_my_rank(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        ranking = []
        for i in Ranking.objects.all():
            if i.user_id == request.user.id:
                tmp = {}
                category_name = Categories.objects.get(id=i.category_id).name
                tmp['points'] = i.rank
                tmp['category_name'] = category_name
                ranking.append(tmp)
        results['message'] = ranking
    return JsonResponse(data=results)

# game_status = 1  // firs player ready to play
# game_status = 2  // first and second players ready to play
# game_status = 3  // one of the players finished game
# game_status = 4  // both players finished game

@csrf_exempt
def add_to_pool(request):
    results = {}
    tmp = {}
    error = {}
    category_id = request.POST['category_id']
    category_id = int(category_id)
    # 1) Proverim esli li user v Pool
    #    1.1) Esli est` proverim nawelsya li sopernik
    #       a) Esli nawelsya otpravlyem dannie
    #    1.2) Esli netu usera v Pool iwem sopernika
    #       a) Esli est` sopernik otpravlyem dannie
    #       b) Esli netu sopernika dobavlyem v Pool
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        rank = Ranking.objects.get(user_id=request.user.id,category_id=category_id).rank
        inPool = 0
        isOpponent = 0
        # check dat user in the pool
        for i in Pool.objects.all():
            if i.user_id == request.user.id and i.category_id == category_id:
                gI = GameInfo.objects.get(id=i.game_info_id)
                inPool = 1
                if gI.user_id_2 != 0 and int(gI.game_status) == 2:
                    opponent = gI.user_id_2
                    game = Game.objects.get(id=gI.game_id)
                    questions = []
                    list = []
                    list.append(game.question_id_1)
                    list.append(game.question_id_2)
                    list.append(game.question_id_3)
                    list.append(game.question_id_4)
                    list.append(game.question_id_5)
                    for i in list:
                        obj = {}
                        obj['id'] = i
                        k = Questions.objects.get(id=i)
                        obj['question'] = k.question_text
                        obj['answer_1'] = k.answer_1
                        obj['answer_2'] = k.answer_2
                        obj['answer_3'] = k.answer_3
                        obj['answer_4'] = k.answer_4
                        obj['correct_answer'] = k.correct_answer
                        questions.append(obj)
                    tmp['success'] = True
                    tmp['text'] = "Your opponent is found"
                    tmp['game_id'] = gI.game_id
                    tmp['opponent_name'] = User.objects.get(id=opponent).first_name
                    tmp['opponent_avatar'] = convertImgToString(Person.objects.get(user_id=opponent).avatar)
                    tmp['opponent_points'] = Ranking.objects.get(user_id=opponent,category_id=category_id).rank
                    tmp['questions'] = questions
                    isOpponent = 1
        if inPool == 0:
            # find opponent in the pool
            for i in Pool.objects.all():
                if i.category_id == category_id and i.user_id != request.user.id:
                    opponent = i.user_id
                    gI = GameInfo.objects.get(id=i.game_info_id)
                    #print type(gI.game_status)
                    gI.user_id_2 = request.user.id
                    gI.game_status = 2
                    gI.save()
                    isOpponent = 1
                    questions = generateQuestions(category_id=category_id)
                    tmp['success'] = True
                    tmp['text'] = "Your opponent is found"
                    tmp['game_id'] = gI.game_id
                    tmp['opponent_name'] = User.objects.get(id=opponent).first_name
                    tmp['opponent_avatar'] = convertImgToString(Person.objects.get(user_id=opponent).avatar)
                    tmp['opponent_points'] = Ranking.objects.get(user_id=opponent,category_id=category_id).rank
                    tmp['questions'] = questions
                    game = Game.objects.get(id=gI.game_id)
                    game.question_id_1 = questions[0]['id']
                    game.question_id_2 = questions[1]['id']
                    game.question_id_3 = questions[2]['id']
                    game.question_id_4 = questions[3]['id']
                    game.question_id_5 = questions[4]['id']
                    game.save()
                    break
        if inPool == 1 and isOpponent != 1:
            tmp['success'] = False
            tmp['text'] = "No opponent"
        #add to pool
        if isOpponent == 0 and inPool == 0:
            user_answer_list_1 = UserAnswerList(user_answer_1=0, user_answer_2=0, user_answer_3=0, user_answer_4=0, user_answer_5=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0)
            user_answer_list_1.save()
            user_answer_list_2 = UserAnswerList(user_answer_1=0, user_answer_2=0, user_answer_3=0, user_answer_4=0, user_answer_5=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0)
            user_answer_list_2.save()
            game = Game(question_id_1=0, question_id_2=0, question_id_3=0, question_id_4=0, question_id_5=0, user1_answer_id=user_answer_list_1.id, user2_answer_id=user_answer_list_2.id)
            game.save()
            gameInfo = GameInfo(user_id_1=request.user.id, user_id_2=0, game_id=game.id, category_id=category_id, game_status=1, point_1=0, point_2=0, date=datetime.datetime.now() + datetime.timedelta(hours=6), pts1_change=0, pts2_change=0)
            gameInfo.save()
            pool = Pool(category_id=category_id, user_id=request.user.id, rank=rank, game_info_id=gameInfo.id)
            pool.save()
            tmp['success'] = False
            tmp['text'] = "Added to pool"
    results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def game_end(request):
    results = {}
    error = {}
    game_id = request.POST['game_id']
    points = request.POST['total']
    user_answer_1 = request.POST['answer1']
    user_answer_2 = request.POST['answer2']
    user_answer_3 = request.POST['answer3']
    user_answer_4 = request.POST['answer4']
    user_answer_5 = request.POST['answer5']
    point_1 = request.POST['point1']
    point_2 = request.POST['point2']
    point_3 = request.POST['point3']
    point_4 = request.POST['point4']
    point_5 = request.POST['point5']
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        gameInfo = GameInfo.objects.get(game_id=game_id)
        game = Game.objects.get(id=game_id)
        answerList = UserAnswerList(id=game.user1_answer_id)
        if gameInfo.user_id_1 == request.user.id:
            gameInfo.point_1 = points
            answerList = UserAnswerList(id=game.user1_answer_id)
        elif gameInfo.user_id_2 == request.user.id:
            gameInfo.point_2 = points
            answerList = UserAnswerList(id=game.user2_answer_id)
        answerList.user_answer_1 = user_answer_1
        answerList.user_answer_2 = user_answer_2
        answerList.user_answer_3 = user_answer_3
        answerList.user_answer_4 = user_answer_4
        answerList.user_answer_5 = user_answer_5
        answerList.point_1 = point_1
        answerList.point_2 = point_2
        answerList.point_3 = point_3
        answerList.point_4 = point_4
        answerList.point_5 = point_5
        if request.user.id == gameInfo.user_id_2 and gameInfo.game_status < 2:
            gameInfo.game_status = int(gameInfo.game_status) + 3
        else:
            gameInfo.game_status = int(gameInfo.game_status) + 1
        answerList.save()
        gameInfo.save()
        game.save()
        tmp = {}
        if gameInfo.game_status == 4 and gameInfo.user_id_2 != 1:
            ranking_update(gameInfo.id)
        try:
            pool = Pool.objects.get(category_id=gameInfo.category_id, user_id=gameInfo.user_id_1, game_info_id=gameInfo.id)
            pool.delete()
        except Pool.DoesNotExist:
            pass
        tmp['success'] = True
        tmp['text'] = "Game end!"
        results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def get_data_from_file(request):
    results = {}
    error = {}
    list = []
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        #file_path = os.path.join(r'C:/Users/Student/Desktop', 'test.xls')
        rb = xlrd.open_workbook('C:/Users/Student/Desktop/test.xls',formatting_info=True)
        #rb = xlrd.open_workbook('C:/Users/abuka/Desktop/test.xls',formatting_info=True)
        sheet = rb.sheet_by_index(0)
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            question = Questions(category_id=row[0], question_text=row[1], answer_1=row[2], answer_2=row[3], answer_3=row[4], answer_4=row[5], correct_answer=row[6], level=row[7])
            question.save()
            list.append(row)
    results['message'] = list
    return JsonResponse(data=results)

@csrf_exempt
def game_result(request):
    results = {}
    error = {}
    game_id = request.POST['game_id']
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        tmp = {}

        k = GameInfo.objects.get(game_id=game_id)
        opponent = k.user_id_1
        tmp['opponent_points'] = k.point_1
        tmp['my_points'] = k.point_2
        if request.user.id == k.user_id_1:
            opponent = k.user_id_2
            tmp['opponent_points'] = k.point_2
            tmp['my_points'] = k.point_1
        tmp['date'] = (k.date).strftime("%Y-%m-%d %H:%M")
        tmp['opponent_name'] = User.objects.get(id=opponent).first_name
        tmp['category_name'] = Categories.objects.get(id=k.category_id).name
        tmp['opponent_avatar'] = convertImgToString(Person.objects.get(user_id=opponent).avatar)
        tmp['opponent_id'] = opponent
        tmp['category_id'] = k.category_id
        if k.game_status != 4:
            tmp['success'] = False
            tmp['text'] = "The second player doesn't finish the game"
        else:
            tmp['success'] = True
            tmp['text'] = "Results"
        results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def kill_search(request):
    results = {}
    error = {}
    tmp = {}
    category_id = request.POST['category_id']
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        k = Pool.objects.get(user_id=request.user.id, category_id=category_id)
        gI = GameInfo.objects.get(id=k.game_info_id)
        if int(gI.game_status) == 2:
            opponent = gI.user_id_2
            game = Game.objects.get(id=gI.game_id)
            questions = []
            list = []
            list.append(game.question_id_1)
            list.append(game.question_id_2)
            list.append(game.question_id_3)
            list.append(game.question_id_4)
            list.append(game.question_id_5)
            for i in list:
                obj = {}
                obj['id'] = i
                q = Questions.objects.get(id=i)
                obj['question'] = q.question_text
                obj['answer_1'] = q.answer_1
                obj['answer_2'] = q.answer_2
                obj['answer_3'] = q.answer_3
                obj['answer_4'] = q.answer_4
                obj['correct_answer'] = q.correct_answer
                questions.append(obj)
            tmp['success'] = True
            tmp['text'] = "Your game is ready"
            tmp['game_id'] = gI.game_id
            tmp['opponent_name'] = User.objects.get(id=opponent).first_name
            tmp['opponent_avatar'] = convertImgToString(Person.objects.get(user_id=opponent).avatar)
            tmp['opponent_points'] = Ranking.objects.get(user_id=opponent, category_id=category_id).rank
            tmp['questions'] = questions
        else:
            g = Game.objects.get(id=gI.game_id)
            ual1 = UserAnswerList(id=g.user1_answer_id)
            ual2 = UserAnswerList(id=g.user2_answer_id)
            ual1.delete()
            ual2.delete()
            g.delete()
            gI.delete()
            k.delete()
            tmp['success'] = False
            tmp['text'] = "Game Deleted"
        results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def login_social_network(request):
    results = {}
    tmp = {}
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    avatar = request.POST['avatar']
    city = request.POST['city']
    id_vk = request.POST['id_vk']
    id_fb = request.POST['id_fb']
    friends = request.POST['friends']
    tmp['success'] = False
    tmp['text'] = "bad"
    if id_fb != '0':
        try:
            user_social = Person.objects.get(fb_id=id_fb)
            user = authenticate(username="fb"+id_fb, password="123")
            login(request, user)
        except Person.DoesNotExist:
            user = User.objects.create_user(username="fb"+id_fb, password="123", first_name=first_name, last_name=last_name)
            user.save()
            person = Person(user_id=user.id, vk_id=id_vk, fb_id=id_fb, city=city, avatar=avatar, total_points=0)
            person.save()
            for i in Categories.objects.all():
                ranking = Ranking(category_id=i.id, user_id=user.id, rank=0)
                ranking.save()
            user = authenticate(username="fb"+id_fb, password="123")
            login(request, user)
        list = json.loads(friends)
        for i in list['friends']:
            try:
                friend = User.objects.get(username="fb"+str(i))
                try:
                    friendship = Friends.objects.get( (Q(user_id_1=friend.id) & Q(user_id_2=user.id)) | (Q(user_id_1=user.id) & Q(user_id_2=friend.id)) )
                except Friends.DoesNotExist:
                    friendship = Friends(user_id_1=user.id, user_id_2=friend.id)
                    friendship.save()
            except:
                pass
        tmp['text'] = "Good"
        tmp['success'] = True
    elif id_vk != '0':
        try:
            user_social = Person.objects.get(vk_id=id_vk)
            user = authenticate(username="vk"+id_vk, password="123")
            login(request, user)
        except Person.DoesNotExist:
            user = User.objects.create_user(username="vk"+id_vk, password="123", first_name=first_name, last_name=last_name)
            user.save()
            person = Person(user_id=user.id, vk_id=id_vk, fb_id=id_fb, city=city, avatar=avatar, total_points=0)
            person.save()
            for i in Categories.objects.all():
                ranking = Ranking(category_id=i.id, user_id=user.id, rank=0)
                ranking.save()
            user = authenticate(username="vk"+id_vk, password="123")
            login(request, user)
        list = json.loads(friends)
        for i in list['friends']:
            try:
                friend = User.objects.get(username="vk"+str(i))
                try:
                    friendship = Friends.objects.get( (Q(user_id_1=friend.id) & Q(user_id_2=user.id)) | (Q(user_id_1=user.id) & Q(user_id_2=friend.id)) )
                except Friends.DoesNotExist:
                    friendship = Friends(user_id_1=user.id, user_id_2=friend.id)
                    friendship.save()
            except User.DoesNotExist:
                pass
        tmp['text'] = "Good"
        tmp['success'] = True
    results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def get_ranking(request):
    results = {}
    error = {}
    list = []
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        for i in Person.objects.order_by('-total_points'):
            user = User.objects.get(id=i.user_id)
            tmp = {}
            tmp['total_points'] = i.total_points
            tmp['first_name'] = user.first_name
            tmp['last_name'] = user.last_name
            tmp['avatar'] = convertImgToString(i.avatar)
            list.append(tmp)
    results['message'] = list
    return JsonResponse(data=results)

@csrf_exempt
def get_friends(request):
    results = {}
    error = {}
    list = []
    msg = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        for i in Friends.objects.all():
            tmp = {}
            if i.user_id_1 == request.user.id:
                user = User.objects.get(id=i.user_id_2)
                person = Person.objects.get(user_id=i.user_id_2)
                tmp['first_name'] = user.first_name
                tmp['last_name'] = user.last_name
                tmp['avatar'] = convertImgToString(person.avatar)
                tmp['total_points'] = person.total_points
                tmp['user_id'] = person.user_id
                list.append(tmp)
            elif i.user_id_2 == request.user.id:
                user = User.objects.get(id=i.user_id_1)
                person = Person.objects.get(user_id=i.user_id_1)
                tmp['first_name'] = user.first_name
                tmp['last_name'] = user.last_name
                tmp['avatar'] = convertImgToString(person.avatar)
                tmp['total_points'] = person.total_points
                tmp['user_id'] = person.user_id
                list.append(tmp)
        list = sorted(list, key=lambda i: i['total_points'])
        list.reverse()
        if len(list) == 0:
            msg['success'] = True
            msg['text'] = "No any friends"
            results['message'] = msg
    results['message'] = list
    return JsonResponse(data=results)

@csrf_exempt
def i_want_to_play_with_friend(request):
    results = {}
    error = {}
    tmp = {}
    friend_id = request.POST['friend_id']
    category_id = request.POST['category_id']
    category_id = int(category_id)
    friend_id = int(friend_id)
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        tmp = {}
        user_answer_list_1 = UserAnswerList(user_answer_1=0, user_answer_2=0, user_answer_3=0, user_answer_4=0, user_answer_5=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0)
        user_answer_list_1.save()
        user_answer_list_2 = UserAnswerList(user_answer_1=0, user_answer_2=0, user_answer_3=0, user_answer_4=0, user_answer_5=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0)
        user_answer_list_2.save()
        game = Game(question_id_1=0, question_id_2=0, question_id_3=0, question_id_4=0, question_id_5=0, user1_answer_id=user_answer_list_1.id, user2_answer_id=user_answer_list_2.id)
        game.save()
        gameInfo = GameInfo(user_id_1=request.user.id, user_id_2=friend_id, game_id=game.id, category_id=category_id, game_status=1, point_1=0, point_2=0, date=datetime.datetime.now() + datetime.timedelta(hours=6), pts1_change=0, pts2_change=0)
        gameInfo.save()
        list = generateQuestions(category_id=gameInfo.category_id)
        tmp['game_id'] = game.id
        tmp['opponent_name'] = User.objects.get(id=gameInfo.user_id_2).first_name
        tmp['opponent_avatar'] = convertImgToString(Person.objects.get(user_id=gameInfo.user_id_2).avatar)
        tmp['opponent_points'] = Person.objects.get(user_id=gameInfo.user_id_2).total_points
        tmp['questions'] = list
        gameInfo.game_status = 0
        gameInfo.save()
        game.question_id_1 = list[0]['id']
        game.question_id_2 = list[1]['id']
        game.question_id_3 = list[2]['id']
        game.question_id_4 = list[3]['id']
        game.question_id_5 = list[4]['id']
        game.save()
        notification(from_user=request.user.id, to_user=friend_id, game_id=gameInfo.game_id)
        tmp['success'] = True
        tmp['text'] = "You invite your friend"
        results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def who_challenge_me(request):
    results = {}
    error = {}
    tmp = {}
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        gameInfo = None
        for i in GameInfo.objects.all():
            if i.user_id_2==request.user.id and i.game_status < 2:
                gameInfo = i
        if gameInfo != None:
            user = User.objects.get(id=gameInfo.user_id_1)
            tmp['full_name'] = user.first_name+" "+user.last_name
            tmp['category_name'] = Categories.objects.get(id=gameInfo.category_id).name
            tmp['game_id'] = gameInfo.game_id
            tmp['success'] = True
            tmp['text'] = "You invite your friend"
        else:
            tmp['success'] = False
            tmp['text'] = "No challenge for you"
        results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def answer_to_challenge(request):
    results = {}
    error = {}
    tmp = {}
    # answer = 1 - NO, wan't to play
    # answer = 2 - Yes, lets play
    answer = request.POST['answer']
    game_id = request.POST['game_id']
    answer = int(answer)
    game_id = int(game_id)
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        gameInfo = GameInfo.objects.get(game_id=game_id)
        game = Game.objects.get(id=game_id)
        user_answer_list_1 = UserAnswerList.objects.get(id=game.user1_answer_id)
        user_answer_list_2 = UserAnswerList.objects.get(id=game.user2_answer_id)
        if answer == 1:
            user_answer_list_2.delete()
            user_answer_list_1.delete()
            game.delete()
            gameInfo.delete()
            tmp['success'] = False
            tmp['text'] = "Game and other deleted"
        elif answer == 2:
            tmp['success'] = True
            tmp['game_id'] = game.id
            tmp['opponent_name'] = User.objects.get(id=gameInfo.user_id_1).first_name
            tmp['opponent_avatar'] = convertImgToString(Person.objects.get(user_id=gameInfo.user_id_1).avatar)
            tmp['opponent_points'] = Person.objects.get(user_id=gameInfo.user_id_1).total_points
            tmp['text'] = "gg wp"
            questions = []
            list = []
            list.append(game.question_id_1)
            list.append(game.question_id_2)
            list.append(game.question_id_3)
            list.append(game.question_id_4)
            list.append(game.question_id_5)
            for i in list:
                obj = {}
                obj['id'] = i
                k = Questions.objects.get(id=i)
                obj['question'] = k.question_text
                obj['answer_1'] = k.answer_1
                obj['answer_2'] = k.answer_2
                obj['answer_3'] = k.answer_3
                obj['answer_4'] = k.answer_4
                obj['correct_answer'] = k.correct_answer
                questions.append(obj)
            tmp['questions'] = questions
        results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def get_top_20(request):
    results = {}
    error = {}
    list = []
    isYou = False
    isOk = False
    position = 1
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        for i in Person.objects.order_by('-total_points'):
            tmp = {}
            if i.id == request.user.id:
                isYou = True
            else:
                isYou = False
            if len(list) < 20 or (len(list) >= 20 and isYou == True):
                user = User.objects.get(id=i.user_id)
                tmp['id'] = i.id
                tmp['first_name'] = user.first_name
                tmp['last_name'] = user.last_name
                tmp['avatar'] = convertImgToString(i.avatar)
                tmp['total_points'] = i.total_points
                tmp['isYou'] = isYou
                tmp['position'] = position
                list.append(tmp)
            position += 1
    results['message'] = list
    return JsonResponse(data=results)

@csrf_exempt
def read_file(request):
    path = 'C:/Users/Student/Desktop/bio.txt'
    f = codecs.open(path, 'r', encoding='utf8')
    #num_lines = sum(1 for line in f)
    lines = f.readlines()
    list = []
    cnt = 1
    correct = -1
    t = {}
    for i in lines:
        if i[0] == '+':
            t['correct_answer'] = cnt - 1
            correct = cnt
        if cnt == 1:
            t['question'] = i[i.find('. ')+2:]
        elif cnt == 2:
            t['answer_1'] = i[i.find(') ')+2:-2]
        elif cnt == 3:
            t['answer_2'] = i[i.find(') ')+2:-2]
        elif cnt == 4:
            t['answer_3'] = i[i.find(') ')+2:-2]
        elif cnt == 5:
            t['answer_4'] = i[i.find(') ')+2:-2]
        elif cnt == 6:
            cnt = 0
            if correct == 6:
                t['correct_answer'] = 4
                t['answer_4'] = i[i.find(') ')+2:-2]
                correct = 0
            list.append(t)
            t = {}
        cnt += 1
    tmp = {}
    tmp['text'] = list
    f.close()
    return JsonResponse(data=tmp)

@csrf_exempt
def from_file_to_db(request):
    category = request.POST['category_id']
    path = 'C:/Users/Student/Desktop/bio.txt'
    f = codecs.open(path, 'r', encoding='utf8')
    #num_lines = sum(1 for line in f)
    lines = f.readlines()
    list = []
    cnt = 1
    correct = -1
    t = {}
    for i in lines:
        if i[0] == '+':
            t['correct_answer'] = cnt - 1
            correct = cnt
        if cnt == 1:
            t['question'] = i[i.find('. ')+2:]
        elif cnt == 2:
            t['answer_1'] = i[i.find(') ')+2:-2]
        elif cnt == 3:
            t['answer_2'] = i[i.find(') ')+2:-2]
        elif cnt == 4:
            t['answer_3'] = i[i.find(') ')+2:-2]
        elif cnt == 5:
            t['answer_4'] = i[i.find(') ')+2:-2]
        elif cnt == 6:
            cnt = 0
            if correct == 6:
                t['correct_answer'] = 4
                t['answer_4'] = i[i.find(') ')+2:-2]
                correct = 0
            #print t['question']
            question = Questions(category_id=category, question_text=t['question'], answer_1=t['answer_1'], answer_2=t['answer_2'], answer_3=t['answer_3'], answer_4=t['answer_4'], correct_answer=t['correct_answer'], level=1)
            question.save()
            list.append(t)
            t = {}
        cnt += 1
    tmp = {}
    tmp['text'] = list
    f.close()
    return JsonResponse(data=tmp)

@csrf_exempt
def play_with_bot(request):
    results = {}
    error = {}
    list = []
    category_id = request.POST['category_id']
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        tmp = {}
        list = generateQuestions(category_id=int(category_id))
        user_answer_list_1 = UserAnswerList(user_answer_1=0, user_answer_2=0, user_answer_3=0, user_answer_4=0, user_answer_5=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0)
        user_answer_list_1.save()
        bot = bot_simulation(questions=list)
        pts_sum = bot[0]['pts']+bot[1]['pts']+bot[2]['pts']+bot[3]['pts']+bot[4]['pts']
        user_answer_list_2 = UserAnswerList(user_answer_1=bot[0]['ans'], user_answer_2=bot[1]['ans'], user_answer_3=bot[2]['ans'], user_answer_4=bot[3]['ans'], user_answer_5=bot[4]['ans'], point_1=bot[0]['pts'], point_2=bot[1]['pts'], point_3=bot[2]['pts'], point_4=bot[3]['pts'], point_5=bot[4]['pts'])
        user_answer_list_2.save()
        game = Game(question_id_1=list[0]['id'], question_id_2=list[1]['id'], question_id_3=list[2]['id'], question_id_4=list[3]['id'], question_id_5=list[4]['id'], user1_answer_id=user_answer_list_1.id, user2_answer_id=user_answer_list_2.id)
        game.save()
        gameInfo = GameInfo(user_id_1=request.user.id, user_id_2=1, game_id=game.id, category_id=category_id, game_status=3, point_1=0, point_2=pts_sum, date=datetime.datetime.now() + datetime.timedelta(hours=6), pts1_change=0, pts2_change=0)
        gameInfo.save()
        tmp['success'] = True
        tmp['game_id'] = game.id
        tmp['opponent_name'] = User.objects.get(id=gameInfo.user_id_2).first_name
        tmp['opponent_avatar'] = convertImgToString(Person.objects.get(user_id=gameInfo.user_id_2).avatar)
        tmp['opponent_points'] = Person.objects.get(user_id=gameInfo.user_id_2).total_points
        tmp['questions'] = list
        results['message'] = tmp
    return JsonResponse(data=results)

# random answer to the questions
def bot_simulation(questions):
    answer_list = []
    for i in xrange(0, 5):
        question = Questions.objects.get(id=questions[i]['id'])
        tmp = {}
        tmp['ans'] = random.randint(1, 4)
        tmp['pts'] = 0
        if tmp['ans'] == question.correct_answer:
            tmp['pts'] = random.randint(1, 10)
        answer_list.append(tmp)
        #print tmp
    return answer_list

# rating calculation for 2 players
def calc_ranking(pts1, pts2, winner):
    # winner = 0 - draw
    # winner = 1 - user1 winner
    # winner = 2 - user2 winner
    w = 0
    if winner == 1:
        w = 1
    elif winner == 0:
        w = 0.5
    E1 = 1.0/(1+10^((pts2-pts1)/400))
    E2 = 1.0/(1+10^((pts1-pts2)/400))
    R1 = getFactor(pts=pts1)*(w-E1)
    R2 = getFactor(pts=pts2)*(1-w-E2)
    tmp = {}
    tmp['user1_pts'] = R1
    tmp['user2_pts'] = R2
    return tmp

def ranking_update(game_info_id):
    gameInfo = GameInfo.objects.get(id=game_info_id)
    person1 = Person.objects.get(user_id=gameInfo.user_id_1)
    person2 = Person.objects.get(user_id=gameInfo.user_id_2)
    person1_categ_rank = Ranking.objects.get(user_id=gameInfo.user_id_1, category_id=gameInfo.category_id)
    person2_categ_rank = Ranking.objects.get(user_id=gameInfo.user_id_2, category_id=gameInfo.category_id)
    ranking1 = Ranking.objects.get(user_id=person1.user_id, category_id=gameInfo.category_id)
    ranking2 = Ranking.objects.get(user_id=person2.user_id, category_id=gameInfo.category_id)
    winner = 0
    if gameInfo.point_1 > gameInfo.point_2:
        winner = 1
    elif gameInfo.point_2 > gameInfo.point_1:
        winner = 2
    result = calc_ranking(ranking1.rank, ranking2.rank, winner)
    person1.total_points += result['user1_pts']
    person2.total_points += result['user2_pts']
    person1_categ_rank.rank += result['user1_pts']
    person2_categ_rank.rank += result['user2_pts']
    gameInfo.pts1_change = result['user1_pts']
    gameInfo.pts2_change = result['user2_pts']
    gameInfo.save()
    gameInfo.save()
    person1.save()
    person2.save()
    person1_categ_rank.save()
    person2_categ_rank.save()

# give coefficient for some pts
def getFactor(pts):
    k = 0
    if pts < 1000:
        k = 30
    elif pts < 1400:
        k = 25
    elif pts < 1800:
        k = 20
    elif pts < 2200:
        k = 15
    elif pts < 2600:
        k = 10
    elif pts < 3000:
        k = 5
    return k

@csrf_exempt
def clear(request):
    tmp = {}
    tmp['ok'] = "true"
    return JsonResponse(data=tmp)

#convert image format to stirng base64 format
def convertImgToString(path):
    #file = cStringIO.StringIO(urllib.urlopen(path).read())
    #stringFormat = base64.b64encode(file.read())
    return path

@csrf_exempt
def search_users(request):
    string = request.POST['string']
    unicodedata.normalize('NFKD', string).encode('ascii','ignore')
    strLow = string.lower()
    strUp = string[0].upper() + string[1::].lower()
    tmp = {}
    results = {}
    users_list = []
    for i in User.objects.filter(Q(first_name__contains=strUp) | Q(first_name__contains=strLow) | Q(last_name__contains=strUp) | Q(last_name__contains=strLow)):
        list = {}
        person = Person.objects.get(user_id=i.id)
        list['first_name'] = i.first_name
        list['last_name'] = i.last_name
        list['avatar'] = person.avatar
        list['city'] = person.city
        list['user_id'] = person.user_id
        list['total_points'] = person.total_points
        if i.id != request.user.id:
            users_list.append(list)
    tmp['text'] = 'No any users'
    tmp['success'] = False
    users_list = sorted(users_list, key=lambda i: i['total_points'])
    users_list.reverse()
    if len(users_list) > 0:
        tmp['text'] = "Ok"
        tmp['success'] = True
        tmp['users'] = users_list
    results['message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def reg_id(request):
    results = {}
    error = {}
    reg_id = request.POST['reg_id']
    if request.user.is_authenticated() == 0:
        error['success'] = False
        error['text'] = "Please, login!"
        results['message'] = error
    else:
        tmp = {}
        tmp['success'] = True
        tmp['text'] = "Good job"
        person = Person.objects.get(user_id=request.user.id)
        person.reg_id = reg_id
        person.save()
        d = GCMDevice(registration_id=reg_id)
        d.save()
        results['message'] = tmp
    return JsonResponse(data=results)

def notification(from_user, to_user, game_id):
    results = {}
    results['text'] = "Very good"
    reg_id = Person.objects.get(user_id=to_user).reg_id
    try:
        device = GCMDevice.objects.get(registration_id=reg_id)
        device.send_message(None, extra={"message": "Give me your parashute!", "title": "Hello, my dear friend!", 'game_id':game_id})
    except GCMDevice.DoesNotExist:
        pass
    return JsonResponse(data=results)
