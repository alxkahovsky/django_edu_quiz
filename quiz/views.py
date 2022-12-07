from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Quiz, Question, QuizCategory
from .quiz_process import QuizEvent


def category_list(request, category_slug=None):
    child_categories = None
    categories = None
    if category_slug:
        category = QuizCategory.objects.get(slug=category_slug)
        child_categories = category.get_children()
    else:
        categories = QuizCategory.objects.filter(is_active=True)
    context = {
        'categories': categories,
        'child_categories': child_categories,
    }
    return render(request, 'quiz/quiz_list.html', context)


def quiz_by_category(request, category_slug):
    category = QuizCategory.objects.get(slug=category_slug)
    quizs = Quiz.objects.filter(category=category)
    context = {
        'quizs': quizs,
        'category': category,
    }
    return render(request, 'quiz/quiz_by_category.html', context)


def quiz_detail(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    quiz_questions = Question.objects.select_related('quiz').filter(quiz=quiz)
    quiz_questions.order_by('id')
    quiz_context = dict([(i, q) for i, q in enumerate(quiz_questions, 1)])
    event = QuizEvent(request, quiz)
    if request.GET:
        query = dict(request.GET)
        question_num = int(query['question_num'][0])
        if question_num in event.quiz_event['questions']:
            event.clear()
            return HttpResponse('Вы нарушили порядок прохождения теста, начните сначала')
        event.add(quiz_context[question_num], query['answers'])
        if question_num == len(quiz_context):
            correct_counter = 0
            incorrect_counter = 0
            for a, ca in zip(event.quiz_event['answers'], quiz.get_answers_map()):
                if a == ca:
                    correct_counter += 1
                else:
                    incorrect_counter += 1
            event.clear()
            return HttpResponse(f'Грац, павильных ответов {correct_counter}, неправильных ответов {incorrect_counter}')
        question_num += 1
        return render(request, 'quiz/quiz.html', {'question': quiz_context[question_num],
                                                  'question_num': question_num})
    else:
        question_num = 1
        question_next = question_num + 1
        return render(request, 'quiz/quiz.html', {'question': quiz_context[question_num],
                      'question_num': question_num})

