
import random


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ..models import QA, UserAnswer


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('backend')
            else:
                form.add_error(None, 'Username o password errati')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def quiz(request):
    error = False

    unanswered_questions = QA.objects.exclude(useranswer__user=request.user, useranswer__answered_correctly=True)

    if not unanswered_questions:
        return render(request, 'quiz_completed.html')

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer:
            # Trova la domanda specifica
            question = QA.objects.get(pk=request.POST.get('question_id'))
            if answer.strip().upper() == question.answer.upper():
                user_answer = UserAnswer.objects.get_or_create(user=request.user, question=question)[0]
                user_answer.answered_correctly = True
                user_answer.save()

                if QA.objects.exclude(useranswer__user=request.user, useranswer__answered_correctly=True).count() == 0:
                    UserAnswer.objects.filter(user=request.user).answered_correctly=0

                if UserAnswer.objects.filter(user=request.user, answered_correctly=False).exists():
                    return redirect('quiz')
                else:
                    UserAnswer.objects.filter(user=request.user).update(answered_correctly=False)
                    return render(request, 'success.html')
            else:
                error = True

    question = random.choice(unanswered_questions)

    context = {'question': question, 'error': error}
    return render(request, 'quiz.html', context)
@login_required
def backend(request):
    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer").upper() == "SI"
        if answer==True:
            risposta="SI"
        else:
            risposta="NO"
        QA.objects.create(question=question, answer=risposta)

    qs = QA.objects.all()
    return render(request, "backend.html", {"qs": qs})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import QA, UserAnswer
from .forms import QAForm


@csrf_exempt
def add_question(request):
    if request.method == 'POST':
        form = QAForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def answer_question(request, id):
    if request.method == 'POST':
        question = QA.objects.get(pk=id)
        answer = request.POST.get('answer', '')
        if answer.strip().upper() == question.answer.upper():
            user_answer = UserAnswer.objects.get_or_create(user=request.user, question=question)[0]
            user_answer.answered_correctly = True
            user_answer.save()
            return JsonResponse({'status': 'ok', 'message': 'Answer is correct'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Answer is incorrect'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})