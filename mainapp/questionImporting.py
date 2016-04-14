import codecs
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mainapp.models import *
import xlrd

@csrf_exempt
def clear(request):
    # for i in range(7385,7585,1):
    #     a = Questions.objects.get(id=i)
    #     a.delete()
    tmp = {}
    tmp['text'] = 'good'
    return JsonResponse(data=tmp)

@csrf_exempt
def read_file(request):
    path = 'C:/Users/abuka/Desktop/entalapp questions(7358)/3.biologiya11-20var(250).txt'
    f = codecs.open(path, 'r', encoding='utf8')
    #num_lines = sum(1 for line in f)
    lines = f.readlines()
    list = []
    cnt = 1
    correct = -1
    t = {}
    for i in lines:
        #i = i.replace("\r","")
        #i = i.replace("\n","")
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
    path = 'C:/Users/abuka/Desktop/entalapp questions(7358)/6.russkiy 3618 part 2.txt'
    f = codecs.open(path, 'r', encoding='utf8')
    #num_lines = sum(1 for line in f)
    lines = f.readlines()
    list = []
    cnt = 1
    correct = -1
    t = {}
    for i in lines:
        #i = i.replace("\r","")
        #i = i.replace("\n","")
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

# @csrf_exempt
# def get_data_from_file(request):
#     results = {}
#     error = {}
#     list = []
#     if request.user.is_authenticated() == 0:
#         error['success'] = False
#         error['text'] = "Please, login!"
#         results['message'] = error
#     else:
#         #file_path = os.path.join(r'C:/Users/Student/Desktop', 'test.xls')
#         rb = xlrd.open_workbook('C:/Users/Abuka/Desktop/Kniga2.xlsx')
#         #rb = xlrd.open_workbook('C:/Users/abuka/Desktop/test.xls',formatting_info=True)
#         sheet = rb.sheet_by_index(0)
#         for rownum in range(1,1428):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#                 list.append(row)
#             question = Questions(category_id=7, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#         for rownum in range(1428,3880):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#             question = Questions(category_id=3, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#         for rownum in range(3880,6504):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#             question = Questions(category_id=2, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#         for rownum in range(6504,8955):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#             question = Questions(category_id=5, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#         for rownum in range(8955, 9402):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#             question = Questions(category_id=8, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#         for rownum in range(9402, 10692):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#             question = Questions(category_id=4, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#         for rownum in range(10692, 12688):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#             question = Questions(category_id=6, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#         for rownum in range(12688, 15823):
#             row = sheet.row_values(rownum)
#             last = row[7]
#             correct = 0
#             if row[9]=='A':
#                 correct = 1
#             elif row[9]=='B':
#                 correct = 2
#             elif row[9]=='C':
#                 correct = 3
#             elif row[9]=='D':
#                 correct = 4
#             elif row[9] == 'E':
#                 last = row[8]
#                 correct = 4
#             question = Questions(category_id=1, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='rus')
#             question.save()
#     results['message'] = list
#     return JsonResponse(data=results)

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
        rb = xlrd.open_workbook('C:/Users/Abuka/Desktop/Kniga1.xlsx')
        #rb = xlrd.open_workbook('C:/Users/abuka/Desktop/test.xls',formatting_info=True)
        sheet = rb.sheet_by_index(0)
        # for rownum in range(1,3018):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #         list.append(row)
        #     question = Questions(category_id=1, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
        # for rownum in range(3018,4182):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #     question = Questions(category_id=3, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
        # for rownum in range(4182,5353):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #     question = Questions(category_id=2, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
        # for rownum in range(5353,6167):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #     question = Questions(category_id=5, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
        # for rownum in range(6167, 7737):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #     question = Questions(category_id=8, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
        # for rownum in range(7737, 9330):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #     question = Questions(category_id=4, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
        # for rownum in range(9331, 10721):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #     question = Questions(category_id=7, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
        # for rownum in range(10721, 12481):
        #     row = sheet.row_values(rownum)
        #     last = row[7]
        #     correct = 0
        #     if row[9]=='A':
        #         correct = 1
        #     elif row[9]=='B':
        #         correct = 2
        #     elif row[9]=='C':
        #         correct = 3
        #     elif row[9]=='D':
        #         correct = 4
        #     elif row[9] == 'E':
        #         last = row[8]
        #         correct = 4
        #     question = Questions(category_id=6, question_text=row[1], answer_1=row[4], answer_2=row[5], answer_3=row[6], answer_4=last, correct_answer=correct, level=0, language='kaz')
        #     question.save()
    results['message'] = list
    return JsonResponse(data=results)