import random
from django.contrib.auth.models import User
from push_notifications.models import GCMDevice, APNSDevice
from mainapp.models import *

# choose 5 random unique questions from all questions
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

# random answer to the questions
def bot_simulation(questions):
    answer_list = []
    for i in xrange(0, 5):
        question = Questions.objects.get(id=questions[i]['id'])
        tmp = {}
        if random.randint(0, 1) == 1:
            tmp['pts'] = random.randint(5, 10)
            tmp['ans'] = question.correct_answer
        else:
            tmp['pts'] = 0
            tmp['ans'] = 1
            if tmp['ans'] == question.correct_answer:
                tmp['ans'] = 2
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
    E1 = 1.0/(1+10**((pts2-pts1)/400.0))
    E2 = 1.0/(1+10**((pts1-pts2)/400.0))
    R1 = getFactor(pts1)*(w-E1)
    R2 = getFactor(pts2)*(1-w-E2)
    tmp = {}
    tmp['user1_pts'] = R1
    tmp['user2_pts'] = R2
    tmp['E1'] = E1
    tmp['E2'] = E2
    return tmp

def ranking_update(game_info_id):
    gameInfo = GameInfo.objects.get(id=game_info_id)
    person1 = Person.objects.get(user_id=gameInfo.user_id_1)
    person2 = Person.objects.get(user_id=gameInfo.user_id_2)
    winner = 0
    if gameInfo.point_1 > gameInfo.point_2:
        winner = 1
    elif gameInfo.point_2 > gameInfo.point_1:
        winner = 2
    result = calc_ranking(person1.total_points, person2.total_points, winner)
    person1.total_points += result['user1_pts']
    person2.total_points += result['user2_pts']
    gameInfo.pts1_change = result['user1_pts']
    gameInfo.pts2_change = result['user2_pts']
    gameInfo.save()
    person1.save()
    person2.save()

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
    else:
        k = 5
    return k

def notification(from_user, to_user, game_id):
    results = "Very good"
    try:
        reg_id = Person.objects.get(user_id=to_user).reg_id
    except Person.DoesNotExist:
        results = "No token_id"
        reg_id = "aAa"
    game_id = str(game_id)
    user = User.objects.get(id=from_user)
    message = user.first_name+" "+ user.last_name+" challenge you!"
    gameInfo = GameInfo.objects.get(id=game_id)
    category_name = Categories.objects.get(id=gameInfo.category_id)
    device = None
    try:
        device = GCMDevice.objects.get(registration_id=reg_id)
    except GCMDevice.DoesNotExist:
        try:
            device = APNSDevice.objects.get(registration_id=reg_id)
        except APNSDevice.DoesNotExist:
            device = None
    if device is not None:
        device.send_message(None, extra={"message": "Challenge!", "title": "Lets punish them!", 'game_id':game_id, 'category_name':"Let's go!"})
    else:
        results = "Very bad"
    return results

