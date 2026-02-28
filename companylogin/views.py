from email import message
import json
import urllib.request
import urllib.error
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from accounts.decorators import require_role

from .models import *
from general_zone.models import *
from admin_zone.models import *
from centerlogin.models import *


@require_role('company')
def com_dashboard(request):
    user_id = request.session.get('com_id')
    Company_data = Company.objects.get(id = user_id)
    tests = Test.objects.all().order_by('-id')
    return render(request,'com_dashboard_modern.html',{'Company_data':Company_data, 'tests': tests})

@require_role('company')
def comLogout(request):
    if request.session.get('com_id'):
        del request.session['com_id']
    return  redirect('homepage')

@require_role('company')
def addExam(request):
    return render(request,'add_exam.html')

@require_role('company')
def saveExam(request):
    if request.method=='POST': 
        name = request.POST.get('exam_name') 
        no = request.POST.get('no_of_questions')  
        marks = request.POST.get('total_marks')  
        exam = Test(test_name = name,no_of_questions=no,total_marks=marks) 
        exam.save()    
        return redirect('com_dashboard')
    return redirect('homepage') 

@require_role('company')
def ongoing_tests(request):
    tests = Test.objects.all()
    return render(request,'ongoing_tests.html',{'tests':tests})

@require_role('company')
def completed_tests(request):
    tests = Test.objects.all()
    return render(request,'completed_tests.html',{'tests':tests})

@require_role('company')
def centers(request):
    centers = Center.objects.all()
    return render(request,'centers.html',{'centers':centers})

@require_role('company')
def addCenter(request):
    if request.method=='POST':
        center_name = request.POST.get('center_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        profile_pic = request.POST.get('profile_pic')
        password = request.POST.get('password')
        center = Center(center_name=center_name,address=address,phone=phone,email=email,profile_pic=profile_pic,password=password)
        center.save()
    return redirect('centers')

@require_role('company')
def questions(request):
    questions = Question.objects.all()
    return render(request,'questions.html',{ 'questions':questions})

@require_role('company')
def addQuestion(request):
    if request.method=='POST':
        test_id = request.POST.get('test_id')
        test_obj = None
        if test_id:
            test_obj = Test.objects.filter(id=test_id).first()
        question = request.POST.get('question')
        option_1 = request.POST.get('option_1')
        option_2 = request.POST.get('option_2')
        option_3 = request.POST.get('option_3')
        option_4 = request.POST.get('option_4')
        correct_option = request.POST.get('correct_option')
        marks = request.POST.get('marks')
        question = Question(
            test=test_obj,
            question=question,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            correct_option=correct_option,
            marks=marks
        )
        question.save()
    return redirect('questions')

@require_role('company')
def companyentry(request):
    return render(request,'com_entry.html')

@require_role('company')
def passcenter(request):
    return render(request,'pass_center.html')


def _build_fallback_questions(topic, difficulty, count):
    """Deterministic fallback if AI key is not configured."""
    fallback = []
    for i in range(1, count + 1):
        fallback.append({
            "question": f"[{difficulty.title()}] {topic}: Sample MCQ {i}",
            "options": [
                f"{topic} concept A{i}",
                f"{topic} concept B{i}",
                f"{topic} concept C{i}",
                f"{topic} concept D{i}",
            ],
            "correct_option": 1
        })
    return fallback


def _generate_ai_questions(topic, difficulty, count):
    """
    Generate MCQs using OpenAI Chat Completions API.
    Returns list[dict] with keys: question, options (4), correct_option (1-4).
    """
    api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
    model = getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        return _build_fallback_questions(topic, difficulty, count), "fallback"

    prompt = (
        "Generate multiple-choice questions in strict JSON only.\n"
        "Return this schema exactly:\n"
        "{ \"questions\": [ { \"question\": \"...\", \"options\": [\"...\",\"...\",\"...\",\"...\"], \"correct_option\": 1 } ] }\n"
        "Rules:\n"
        f"- topic: {topic}\n"
        f"- difficulty: {difficulty}\n"
        f"- count: {count}\n"
        "- exactly 4 options\n"
        "- correct_option must be integer 1..4\n"
        "- no markdown\n"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an exam question generator. Output valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise ValueError(f"AI API error: {detail[:250]}")
    except Exception as exc:
        raise ValueError(f"AI request failed: {str(exc)}")

    try:
        data = json.loads(body)
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        questions = parsed.get("questions", [])
    except Exception as exc:
        raise ValueError(f"Invalid AI response format: {str(exc)}")

    valid = []
    for q in questions:
        question = str(q.get("question", "")).strip()
        options = q.get("options", [])
        correct_option = q.get("correct_option", 1)

        if not question or not isinstance(options, list) or len(options) != 4:
            continue

        try:
            correct_option = int(correct_option)
        except Exception:
            correct_option = 1

        if correct_option < 1 or correct_option > 4:
            correct_option = 1

        valid.append({
            "question": question[:512],
            "options": [str(options[0])[:256], str(options[1])[:256], str(options[2])[:256], str(options[3])[:256]],
            "correct_option": correct_option,
        })

    if not valid:
        raise ValueError("AI returned no valid questions.")

    return valid[:count], "openai"


@require_role('company')
def generate_ai_questions(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required."}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON payload."}, status=400)

    topic = str(payload.get("topic", "")).strip()
    exam_id = payload.get("exam_id")
    difficulty = str(payload.get("difficulty", "medium")).strip().lower()
    count = payload.get("count", 5)
    marks = payload.get("marks", 1)

    if not topic:
        return JsonResponse({"success": False, "error": "Topic is required."}, status=400)

    if difficulty not in {"easy", "medium", "hard"}:
        difficulty = "medium"

    try:
        exam_id = int(exam_id)
        count = int(count)
        marks = int(marks)
    except Exception:
        return JsonResponse({"success": False, "error": "Exam, count and marks must be valid integers."}, status=400)

    exam_obj = Test.objects.filter(id=exam_id).first()
    if not exam_obj:
        return JsonResponse({"success": False, "error": "Selected exam not found."}, status=404)

    if count < 1 or count > 20:
        return JsonResponse({"success": False, "error": "Count must be between 1 and 20."}, status=400)
    if marks < 1 or marks > 20:
        return JsonResponse({"success": False, "error": "Marks must be between 1 and 20."}, status=400)

    try:
        generated, source = _generate_ai_questions(topic=topic, difficulty=difficulty, count=count)
    except ValueError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)

    return JsonResponse({
        "success": True,
        "message": f"{len(generated)} questions generated. Review and save to exam.",
        "count": len(generated),
        "source": source,
        "exam": {"id": exam_obj.id, "name": exam_obj.test_name},
        "questions": [
            {
                "question": q["question"],
                "option_1": q["options"][0],
                "option_2": q["options"][1],
                "option_3": q["options"][2],
                "option_4": q["options"][3],
                "correct_option": int(q["correct_option"]),
                "marks": marks,
            }
            for q in generated
        ],
    })


@require_role('company')
def save_ai_questions(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required."}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON payload."}, status=400)

    exam_id = payload.get("exam_id")
    questions = payload.get("questions", [])

    try:
        exam_id = int(exam_id)
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid exam id."}, status=400)

    exam_obj = Test.objects.filter(id=exam_id).first()
    if not exam_obj:
        return JsonResponse({"success": False, "error": "Selected exam not found."}, status=404)

    if not isinstance(questions, list) or not questions:
        return JsonResponse({"success": False, "error": "No questions provided."}, status=400)

    created = 0
    for item in questions:
        q_text = str(item.get("question", "")).strip()[:512]
        opt1 = str(item.get("option_1", "")).strip()[:256]
        opt2 = str(item.get("option_2", "")).strip()[:256]
        opt3 = str(item.get("option_3", "")).strip()[:256]
        opt4 = str(item.get("option_4", "")).strip()[:256]

        if not q_text or not opt1 or not opt2 or not opt3 or not opt4:
            continue

        try:
            correct_option = int(item.get("correct_option", 1))
        except Exception:
            correct_option = 1
        if correct_option < 1 or correct_option > 4:
            correct_option = 1

        try:
            marks = int(item.get("marks", 1))
        except Exception:
            marks = 1
        if marks < 1:
            marks = 1

        Question.objects.create(
            test=exam_obj,
            question=q_text,
            option_1=opt1,
            option_2=opt2,
            option_3=opt3,
            option_4=opt4,
            correct_option=f"Option {correct_option}",
            marks=marks,
        )
        created += 1

    if created == 0:
        return JsonResponse({"success": False, "error": "No valid questions to save."}, status=400)

    return JsonResponse({
        "success": True,
        "message": f"{created} questions saved and attached to exam '{exam_obj.test_name}'.",
        "count": created,
        "exam_id": exam_obj.id,
    })
