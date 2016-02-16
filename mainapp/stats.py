from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mainapp.models import GameInfo, Categories, UserAnswerList

# how much game was played in which time
@csrf_exempt
def data_by_time(request):
    tmp = {}
    time = {}
    time['morning'] = 0
    time['day'] = 0
    time['evening'] = 0
    time['night'] = 0
    day = [0,0,0,0,0,0,0]
    gameInfo = GameInfo.objects.all()
    for i in gameInfo:
        hour = i.date.hour
        if hour > 5 and hour <= 10:
            time['morning'] += 1
        elif hour > 10 and hour <= 17:
            time['day'] += 1
        elif hour > 17 and hour <= 23:
            time['evening'] += 1
        else:
            time['night'] += 1
        d = i.date.weekday()

        day[d] += 1
    tmp['time'] = time
    tmp['day'] = day
    return JsonResponse(data=tmp)

@csrf_exempt
def game_stats(request):
    games = {}
    tmp = {}
    subject = [0,0,0,0]
    games['pve'] = 0
    games['pvp'] = 0
    for i in GameInfo.objects.all():
        if i.user_id_2 == 1:
            games['pve'] += 1
        else:
            games['pvp'] += 1

    for i in GameInfo.objects.all():
        subject[i.category_id] += 1

    tmp['games'] = games
    tmp['subject'] = subject
    return JsonResponse(data=tmp)

@csrf_exempt
def data_by_answers(request):
    tmp = {}
    answers = {}
    answers['Correct'] = 0
    answers['Incorrect'] = 0
    for i in UserAnswerList.objects.all():
        if i.point_1 or i.point_2 or i.point_3 or i.point_4 or i.point_5:
            answers['Correct'] += 1
        else:
            answers['Incorrect'] += 1
    tmp['answers'] = answers
    return JsonResponse(data=tmp)
