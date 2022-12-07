from django.urls import path, re_path, include
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.category_list, name='catogory_quiz_list'),
    path('<slug:category_slug>/', views.category_list, name='category_quiz_list_by_category'),
    path('quiz/<slug:quiz_slug>', views.quiz_detail, name='quiz_detail'),
    path('quiz_by/<slug:category_slug>', views.quiz_by_category, name='quiz_by_category')
]
