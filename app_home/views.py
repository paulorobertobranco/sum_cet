from django.shortcuts import render


def home(request):
    data = {
        'active_link': 'home'
    }
    return render(request, 'app_home/home.html', data)
