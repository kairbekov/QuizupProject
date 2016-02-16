import codecs
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import xlrd
from mainapp.models import *

@csrf_exempt
def clear(request):
    #for i in range(3275,4008,1):
    #    a = Questions.objects.get(id=i)
    #    a.delete()
    tmp = {}
    tmp['text'] = 'good'
    return JsonResponse(data=tmp)

@csrf_exempt
def read_file(request):
    path = 'C:/Users/abuka/Desktop/entalapp questions(7358)/6.russkiy 3618 part 1.txt'
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
    # don't forget about CATEGORY_ID
    # don't forget about URL to file
    category = request.POST['category_id']
    path = 'C:/Users/abuka/Desktop/entalapp questions(7358)/6.russkiy 3618 part 1.txt'
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
