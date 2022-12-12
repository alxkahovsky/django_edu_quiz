from django.contrib import admin
from .models import Question, Quiz, QuizCategory


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    show_change_link = True
    readonly_fields = ['created', 'updated']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['question', 'quiz', ('answer_a', 'answer_b', 'answer_c', 'answer_d'),
              'correct_answer', ('created', 'updated'), 'is_active']
    list_display = ['question', 'quiz', 'is_active']
    readonly_fields = ['created', 'updated']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'description', 'category']
    list_display = ['name', 'slug', 'description']
    inlines = [QuestionInline]
    readonly_fields = ['created', 'updated']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    model = QuizCategory
    readonly_fields = ['created', 'updated']
    prepopulated_fields = {'slug': ('name',)}