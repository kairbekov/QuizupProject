from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from mainapp.models import *


@csrf_exempt
def login_view(request):
    results = {}
    tmp = {}
    username = request.POST['username']
    password = request.POST['password']
    tmp['Success'] = False
    tmp['Text'] = "Bla bla"
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            request.user = user
            login(request, user)
            tmp['Success'] = True
            tmp['Text'] = "Your account is ok"
            #return HttpResponse("Your account is ok.")
        else:
            tmp['Success'] = True
            tmp['Text'] = "Your account is disabled"
            #return HttpResponse("Your account is disabled.")
    else:
         #print "Invalid login details: {0}, {1}".format(username, password)
         tmp['Success'] = False
         tmp['Text'] = "Invalid login details supplied"
         #return HttpResponse("Invalid login details supplied.")
    results['Message'] = tmp
    #print(request.META['csrftoken'])
    return JsonResponse(data=results)

@csrf_exempt
def logout_view(request):
    results = {}
    tmp = {}
    tmp['Success'] = True
    tmp['Text'] = " "
    results['Message'] = tmp
    logout(request)
    return JsonResponse(data=results)


@csrf_exempt
def registration(request):
    results = {}
    tmp = {}
    tmp['Success'] = False
    tmp['Text'] = "Current user is already exist"
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    #user_check1 = User.objects.get(username=username)
    #user_check2 = User.objects.get(email=email)
    if username and password and email:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user = authenticate(username=username, password=password)
        login(request,user)
        for i in Categories.objects.all():
            ranking = Ranking(category_id=i.id, user_id=user.id, rank=1000)
            ranking.save()
        tmp['Success'] = True
        tmp['Text'] = " "
    results['Message'] = tmp;
    return JsonResponse(data=results)

@csrf_exempt
def users_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "please login!"
        results['Message'] = error
    else:
        user_list = []
        for i in User.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['username'] = i.username
            tmp['email'] = i.email
            tmp['password'] = i.password
            user_list.append(tmp)
        results['Message'] = user_list
    return JsonResponse(data=results)

@csrf_exempt
def category_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        categroy_list = []
        for i in Categories.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['category'] = i.name
            tmp['subcategory'] = i.subcategory
            categroy_list.append(tmp)
        results['Categories'] = categroy_list
    #print(request)
    return JsonResponse(data=results)

@csrf_exempt
def add_category(request):
    results = {}
    tmp = {}
    name = request.GET['name']
    tmp['Success'] = False
    tmp['Text'] = "Not correct"
    if request.user.is_authenticated() == 0:
        tmp['Text'] = "Please, login!"

    if name is not None and request.user.is_authenticated():
        category = Categories(name=name)
        category.save()
        tmp['Success'] = True
        tmp['Text'] = " "
    results['Message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def question_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        question_list = []
        for i in Questions.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['category_id'] = i.category_id
            tmp['question_text'] = i.question_text
            tmp['answer_1'] = i.answer_1
            tmp['answer_2'] = i.answer_2
            tmp['answer_3'] = i.answer_3
            tmp['answer_4'] = i.answer_4
            tmp['correct_answer'] = i.correct_answer
            question_list.append(tmp)
        results['Message'] = question_list
    return JsonResponse(data=results)

@csrf_exempt
def add_question(request):
    results = {}
    tmp = {}
    tmp['Success'] = False
    tmp['Text'] = "Not correct"
    category_id = request.GET['category_id']
    question_text = request.GET['question_text']
    answer_1 = request.GET['answer_1']
    answer_2 = request.GET['answer_2']
    answer_3 = request.GET['answer_3']
    answer_4 = request.GET['answer_4']
    correct_answer = request.GET['correct_answer']
    if category_id and question_text and answer_1 and answer_2 and answer_3 and answer_4 and correct_answer:
        question = Questions(category_id=category_id, question_text=question_text, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4, correct_answer=correct_answer)
        question.save()
        tmp['Text'] = " "
        tmp['Success'] = True
    results['Message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def delete_category(request):
    results = {}
    tmp = {}
    id = request.GET['id']
    tmp['Success'] = False
    tmp['Text'] = "Not correct"
    if request.user.is_authenticated() == 0:
        tmp['Text'] = "Please, login!"

    if id is not None and request.user.is_authenticated():
        category = Categories(id=id)
        category.delete()
        tmp['Success'] = True
        tmp['Text'] = " "
    results['Message'] = tmp;
    return JsonResponse(data=results)

@csrf_exempt
def pool(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        pool = []
        for i in Pool.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['category_id'] = i.category_id
            tmp['user_id'] = i.user_id
            tmp['rank'] = i.rank
            pool.append(tmp)
        results['Message'] = pool
    return JsonResponse(data=results)

@csrf_exempt
def add_to_pool(request):
    results = {}
    tmp = {}
    category_id = request.POST['category_id']
    category_id = int(category_id)
    user_id = request.user.id
    user2_id = -1
    tmp['success'] = False
    tmp['text'] = "Not correct"
    if request.user.is_authenticated() == 0:
        tmp['text'] = "Please, login!"
    if category_id is not None and request.user.is_authenticated():
        ranking = Ranking.objects.get(category_id=category_id, user_id=user_id)
        for i in Pool.objects.all():
            if i.user_id!=user_id and i.category_id==category_id and abs(i.rank-ranking.rank)<100:
                user2_id = i.user_id
                break
        if user2_id != -1:
            #pool = Pool.objects.get(user_id=user2_id, category_id=category_id)
            user1_answer = UserAnswerList(user_answer_1=0, user_answer_2=0, user_answer_3=0, user_answer_4=0, user_answer_5=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0)
            user2_answer = UserAnswerList(user_answer_1=0, user_answer_2=0, user_answer_3=0, user_answer_4=0, user_answer_5=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0)
            user1_answer.save()
            user2_answer.save()
            game = Game(question_id_1=1, question_id_2=2, question_id_3=3, question_id_4=5, question_id_5=1, user1_answer_id=user1_answer.id, user2_answer_id=user2_answer.id)
            game.save()
            newGame = GameInfo(user_id_1=user_id, user_id_2=user2_id, category_id=category_id, game_status=1, point_1=0, point_2=0, game_id=game.id)
            newGame.save()
            question_list = generateQuestions()
            tmp['success'] = True
            tmp['text'] = "Your opponent id = "+str(user2_id)
            tmp['game_id'] = newGame.id
            tmp['opponent_avatar'] = "http://cdn.indiewire.com/dims4/INDIEWIRE/2f993ce/2147483647/thumbnail/120x80%3E/quality/75/?url=http%3A%2F%2Fd1oi7t5trwfj5d.cloudfront.net%2F91%2Fa9%2F5a2c1503496da25094b88e9eda5f%2Favatar.jpeg"
            tmp['opponent_name'] = User.objects.get(id=user2_id).first_name
            tmp['opponent_id'] = user2_id
            tmp['opponent_city'] = "NYC"
            tmp['opponent_points'] = Ranking.objects.get(user_id=user2_id,category_id=category_id).rank
            tmp['Questions'] = question_list
        else:
            pool = Pool(category_id=category_id, user_id=user_id, rank=ranking.rank)
            pool.save()
            tmp['text'] = "No opponent, w8 pls"
            tmp['success'] = False
    results['Message'] = tmp
    return JsonResponse(data=results)

@csrf_exempt
def rank_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        ranking = []
        for i in Ranking.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['category_id'] = i.category_id
            tmp['user_id'] = i.user_id
            tmp['rank'] = i.rank
            ranking.append(tmp)
        results['Message'] = ranking
    return JsonResponse(data=results)


@csrf_exempt
def friend_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        friends = []
        for i in Friends.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['user_id_1'] = i.user_id_1
            tmp['user_id_2'] = i.user_id_2
            friends.append(tmp)
        results['Message'] = friends
    return JsonResponse(data=results)

@csrf_exempt
def game_info(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        gameInfo = []
        for i in GameInfo.objects.all():
            tmp = {}
            tmp['id'] = i.id
            tmp['user_id_1'] = i.user_id_1
            tmp['user_id_2'] = i.user_id_2
            tmp['game_id'] = i.game_id
            tmp['category_id'] = i.category_id
            tmp['game_status'] = i.game_status
            tmp['point_1'] = i.point_1
            tmp['point_2'] = i.point_2
            gameInfo.append(tmp)
        results['Message'] = gameInfo
    return JsonResponse(data=results)

@csrf_exempt
def get_my_profile(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        profile = {}
        tmp = User.objects.get(id = request.user.id)
        profile['id'] = tmp.id
        profile['first_name'] = tmp.first_name
        profile['last_name'] = tmp.last_name
        results['Message'] = profile
    return JsonResponse(data=results)

@csrf_exempt
def get_my_category_list(request):
    results = {}
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        category_list = []
        for i in GameInfo.objects.filter(Q(user_id_1 = request.user.id) | Q(user_id_2 = request.user.id)):
            tmp = {}
            category = Categories.objects.get(id=i.category_id)
            tmp['category_name'] = category.name
            tmp['subcategory_name'] = category.subcategory
            tmp['id'] = category.id
            category_list.append(tmp)
        results['Message'] = category_list
    return JsonResponse(data=results)


@csrf_exempt
def get_my_rank_by_category(request):
    results = {}
    error = {}
    category_id = request.POST['id']
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        ranking = {}
        tmp = Ranking.objects.get(user_id=request.user.id, category_id=category_id)
        ranking['category_name'] = Categories.objects.get(id=tmp.category_id).name
        ranking['category_point'] = tmp.rank
        ranking['category_id'] = Categories.objects.get(id=tmp.category_id).id
        results['Message'] = ranking
    return JsonResponse(data=results)

@csrf_exempt
def get_played_games_list(request):
    results = {}
    list = []
    error = {}
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
    else:
        for i in GameInfo.objects.filter(Q(user_id_1=request.user.id) | Q(user_id_2=request.user.id)):
            opponent = User.objects.get(id=i.user_id_1)
            if i.user_id_1 == request.user.id:
                opponent = User.objects.get(id=i.user_id_2)
            games_list = {}
            games_list['opponent_name'] = opponent.first_name
            games_list['game_status'] = i.game_status
            games_list['opponent_level'] = Ranking.objects.get(user_id=opponent.id, category_id=i.category_id).rank
            games_list['category'] = Categories.objects.get(id=i.category_id).name
            games_list['game_info_id'] = i.id
            list.append(games_list)
        results['Message'] = list
    return JsonResponse(data=results)


@csrf_exempt
def get_played_game_info(request):
    results = {}
    list = []
    error = {}
    game_info_id = request.POST['id']
    if request.user.is_authenticated() == 0:
        error['Success'] = False
        error['Text'] = "Please, login!"
        results['Message'] = error
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
        results['Message'] = list
    return JsonResponse(data=results)


def generateQuestions():
    list = []
    for i in Questions.objects.all():
        tmp = {}
        tmp['question'] = i.question_text
        tmp['answer_1'] = i.answer_1
        tmp['answer_2'] = i.answer_2
        tmp['answer_3'] = i.answer_3
        tmp['answer_4'] = i.answer_4
        tmp['correct_answer'] = i.correct_answer
        list.append(tmp)
        if list.__len__() >= 5: break
    return list


