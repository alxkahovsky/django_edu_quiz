from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Quiz, Question, QuizCategory
from .quiz_process import QuizEvent, QuizSetProcess
from django.contrib.auth.decorators import login_required


@login_required
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


@login_required
def quiz_by_category(request, category_slug):
    category = QuizCategory.objects.get(slug=category_slug)
    quizs = list(Quiz.objects.filter(category=category).order_by('id'))
    process_quiz = QuizSetProcess(request)
    if process_quiz.quiz_set['quizs'] == []:
        context = {
            'quiz': quizs[0],
            'category': category,
            'process_quiz': process_quiz.quiz_set,
        }
        return render(request, 'quiz/quiz_by_category.html', context)
    else:
        last_passed_quiz = Quiz.objects.get(id=process_quiz.quiz_set['quizs'][-1])
        if quizs.index(last_passed_quiz) != len(quizs) - 1:
            next_quiz_index = quizs.index(last_passed_quiz) + 1
            context = {
                'quiz': quizs[next_quiz_index],
                'category': category,
                'process_quiz': process_quiz.quiz_set,
            }
            return render(request, 'quiz/quiz_by_category.html', context)
    user = request.user
    quiz_results = zip(quizs, process_quiz.quiz_set['quiz_result'])
    context = {
        'user': user,
        'category': category,
        'quiz_results': quiz_results,
    }
    process_quiz.clear()
    return render(request, 'quiz/quiz_result.html', context)


@login_required
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
            process_quiz = QuizSetProcess(request)
            a = event.quiz_event['answers']
            r = quiz.check_user_result(a)
            process_quiz.add(quiz, True, r)
            event.clear()
            return redirect('quiz:quiz_by_category', quiz.category.last().slug)
        question_num += 1
        return render(request, 'quiz/quiz.html', {'question': quiz_context[question_num],
                                                  'question_num': question_num})
    else:
        question_num = 1
        question_next = question_num + 1
        return render(request, 'quiz/quiz.html', {'question': quiz_context[question_num],
                      'question_num': question_num})

