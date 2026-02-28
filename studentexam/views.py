from django.shortcuts import render
from datetime import datetime, timedelta
from companylogin.models import *
from django.http import JsonResponse
from companylogin.models import Question
# import table from models.py which will store question for all 

# Create your views here.
def studhome(req):
    return render(req,'stud_home.html')
def instruction(req):
    return render(req,'instruction.html')

def running(req):
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)  # Set the end time to 1 hour from now

    return render(req, 'running_exam.html', {
        'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),  # Format the time as a string
        'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
    })
def over(req):
    return render(req,'submit.html')


# this is for exam conducting exam using ajax technology 


def get_next_question(request, current_question_id):
    try:
        next_question = Question.objects.get(id=current_question_id + 1)
    except Question.DoesNotExist:
        next_question = None
    
    if next_question:
        data = {
            'id':next_question.id,
            'question_text': next_question.question,
            'option1': next_question.option_1,
            'option2': next_question.option_2,
            'option3': next_question.option_3,
            'option4': next_question.option_4,
            'size':Question.objects.count()
        }
    else:
        data = {
            'id':'',
            'question_text': "No more questions",
            'option1': '',
            'option2': '',
            'option3': '',
            'option4': '',
            'size':Question.objects.count()
        }

    return JsonResponse(data)

def get_previous_question(request, current_question_id):
    if current_question_id > 1:
        previous_question = Question.objects.get(id=current_question_id - 1)
    else:
        previous_question = None

    if previous_question:
        data = {
            'id':previous_question.id,
            'question_text': previous_question.question,
            'option1': previous_question.option_1,
            'option2': previous_question.option_2,
            'option3': previous_question.option_3,
            'option4': previous_question.option_4,
        }
    else:
        data = {
            'id':'',
            'question_text': "No previous questions",
            'option1': '',
            'option2': '',
            'option3': '',
            'option4': '',
        }

    return JsonResponse(data)
