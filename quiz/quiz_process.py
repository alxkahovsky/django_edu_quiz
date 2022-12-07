from django.conf import settings


class QuizEvent(object):
    """Смотрим quiz_event :{id_quiz:{id_question:answer}} """
    def __init__(self, request, quiz):
        self.session = request.session
        quiz_event = self.session.get(settings.QUIZ_EVENT_SESSION_ID)

        if not quiz_event:
            quiz_event = self.session[settings.QUIZ_EVENT_SESSION_ID] = {'questions': [],
                                                                         'answers': []}
        self.quiz_event = quiz_event

    def add(self, question, answer):
        question_id = question.id
        questions_list = self.quiz_event['questions']
        answers_list = self.quiz_event['answers']
        if question_id not in questions_list:
            questions_list.append(question_id)
            answers_list.append(answer)
            self.quiz_event['questions'] = questions_list
            self.quiz_event['answers'] = answers_list
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.QUIZ_EVENT_SESSION_ID]
        self.save()


class QuizSetProcess(object):
    def __init__(self, request):
        self.session = request.session
        quiz_set = self.session.get(settings.QUIZ_SET_SESSION_ID)
        if not quiz_set:
            quiz_set = self.session[settings.QUIZ_SET_SESSION_ID] = {'quizs': [],
                                                                           'process': [],
                                                                            'user_answer_map': []}
        self.quiz_set = quiz_set

    def add(self, quiz, process, answer_map):
        quizs_list = self.quiz_set['quizs']
        process_list = self.quiz_set['process']
        answers_list = self.quiz_set['user_answer_map']
        if quiz.id not in quizs_list:
            quizs_list.append(quiz.id)
            process_list.append(process)
            answers_list.append(answer_map)
            self.quiz_set['quizs'] = quizs_list
            self.quiz_set['process'] = process_list
            self.quiz_set['user_answer_map'] = answer_map
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.QUIZ_SET_SESSION_ID]
        self.save()
