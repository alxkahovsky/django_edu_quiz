from django.contrib import admin
from .models import Question, Quiz, QuizCategory


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    show_change_link = True

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'description', 'category']
    list_display = ['name', 'slug', 'description',]
    inlines = [QuestionInline]

@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    model = QuizCategory