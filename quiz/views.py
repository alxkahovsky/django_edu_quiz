from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Quiz, Question


def quiz_list(request):
    quizs = Quiz.objects.filter(is_active=True)
    return HttpResponse(quizs)

def quiz_detail(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    quiz_questions = Question.objects.select_related('quiz').filter(quiz=quiz)
    return HttpResponse(quiz_questions)



