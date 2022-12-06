from django.db import models
from multiselectfield import MultiSelectField
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils import timezone


class UpdatedCreatedActive(models.Model):
    created = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')
    updated = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Дата ред-ия записи')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    class Meta:
        abstract = True


class QuizCategory(MPTTModel, UpdatedCreatedActive):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Подкатегория тестов')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='Уникальная строка')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='Категория тестов')

    def __str__(self):
        return f'Категория {self.name}'


class Quiz(UpdatedCreatedActive):
    name = models.CharField(max_length=200, verbose_name='Название теста')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Уникальная строка')
    description = models.TextField(max_length=1000, verbose_name='Описание теста')
    category = TreeManyToManyField(QuizCategory, blank=True, symmetrical=False, related_name='quizs',
                                   verbose_name='Категория->Подкатегория')

    def __str__(self):
        return f'{self.name}'


class AnswerChoises(models.TextChoices):
    ANSWER_A = 'A', 'Вариант A',
    ANSWER_B = 'B', 'Вариант B',
    ANSWER_C = 'C', 'Вариант C',
    ANSWER_D = 'D', 'Вариант D',


class Question(UpdatedCreatedActive):
    question = models.CharField(max_length=200, verbose_name='Вопрос')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)
    answer_a = models.CharField(max_length=200, verbose_name='Вариант ответа A', default='')
    answer_b = models.CharField(max_length=200, verbose_name='Вариант ответа B', default='')
    answer_c = models.CharField(max_length=200, verbose_name='Вариант ответа C', default='')
    answer_d = models.CharField(max_length=200, verbose_name='Вариант ответа D', default='')
    correct_answer = MultiSelectField(choices=AnswerChoises.choices, max_length=8, verbose_name='Правильные варианты')


    def __str__(self):
        return f'Вопрос №{self.id}'

