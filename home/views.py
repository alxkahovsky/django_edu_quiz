from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        context = {
            'login': True,
            'username': username
        }
        return render(request, 'home/home.html', context)
    else:
        context = {
            'login': False
        }
        return render(request, 'home/home.html', context)
