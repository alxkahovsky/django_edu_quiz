from django.urls import path, re_path, include
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<slug:quiz_slug>', views.quiz_detail, name='quiz_detail')
]
