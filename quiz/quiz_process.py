from django.conf import settings
from .models import Quiz, Question
from django.core.handlers.wsgi import WSGIRequest


class QuizEvent(object):
    """Класс для хранения процесса прохождения отдельного теста в сессии"""
    def __init__(self, request: WSGIRequest, quiz: Quiz):
        self.session = request.session
        quiz_event = self.session.get(settings.QUIZ_EVENT_SESSION_ID)

        if not quiz_event:
            quiz_event = self.session[settings.QUIZ_EVENT_SESSION_ID] = {'questions': [],
                                                                         'answers': []}
        self.quiz_event = quiz_event

    def add(self, question: Question, answer: str) -> None:
        question_id = question.id
        questions_list = self.quiz_event['questions']
        answers_list = self.quiz_event['answers']
        if question_id not in questions_list:
            self.quiz_event['questions'].append(question_id)
            self.quiz_event['answers'].append(answer)
            self.save()

    def save(self) -> None:
        self.session.modified = True

    def clear(self) -> None:
        del self.session[settings.QUIZ_EVENT_SESSION_ID]
        self.save()


class QuizSetProcess(object):
    """Класс для хранения процесса прохождения цепочки тестов"""
    def __init__(self, request):
        self.session = request.session
        quiz_set = self.session.get(settings.QUIZ_SET_SESSION_ID)
        if not quiz_set:
            quiz_set = self.session[settings.QUIZ_SET_SESSION_ID] = {'quizs': [],
                                                                           'process': [],
                                                                            'quiz_result': []}
        self.quiz_set = quiz_set

    def add(self, quiz: Quiz, process: bool, quiz_result: dict) -> None:
        quizs_list = self.quiz_set['quizs']
        process_list = self.quiz_set['process']
        answers_list = self.quiz_set['quiz_result']
        if quiz.id not in quizs_list:
            self.quiz_set['quizs'].append(quiz.id)
            self.quiz_set['process'].append(process)
            self.quiz_set['quiz_result'].append(quiz_result)
            self.save()

    def save(self) -> None:
        self.session.modified = True

    def clear(self) -> None:
        del self.session[settings.QUIZ_SET_SESSION_ID]
        self.save()
