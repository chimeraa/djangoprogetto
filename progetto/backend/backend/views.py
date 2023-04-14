from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ..models import QA
import random


@csrf_exempt
def quiz(request):

    # Ottieni tutte le domande non risposte correttamente
    unanswered_qs = QA.objects.filter(correct_answer=False)

    # Se non ci sono domande non risposte correttamente, l'utente ha completato il quiz
    if not unanswered_qs.exists():
        QA.objects.all().update(correct_answer=False)
        return render(request, 'success.html')

    # Scegli una domanda casuale tra quelle non risposte correttamente
    question = unanswered_qs.order_by('?').first()

    if request.method == 'POST':
        user_answer = request.POST.get('user_answer')

        # Se l'utente ha risposto correttamente, imposta il valore di correct_answer a True
        if user_answer.lower() == question.answer.lower():
            question.correct_answer = True
            question.save()
            return JsonResponse({'is_correct': True})

        # Se l'utente ha risposto in modo errato, ritorna una nuova domanda casuale
        else:
            new_question = unanswered_qs.exclude(pk=question.pk).order_by('?').first()
            return JsonResponse({'error': 'Risposta sbagliata', 'question': new_question.question})

    # Se la richiesta è una GET, mostra la domanda e il box per la risposta
    return render(request, 'quiz.html', {'question': question})
def backend(request):
    if request.method == "POST":
        question = request.POST.get("question")
        answer = request.POST.get("answer").upper() == "SI"
        QA.objects.create(question=question, answer=answer)

    qs = QA.objects.all()
    return render(request, "backend.html", {"qs": qs})
