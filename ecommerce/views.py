from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site


def homeView(request):
    list = {
        'registration': 'https://www.cleverange.com/api/registration/',
        'login': 'https://www.cleverange.com/api/login/',
        'logout': 'https://www.cleverange.com/api/logout/'
    }
    context = {
        'lists': list
    }
    return render(request, 'index.html', context)