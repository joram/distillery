from django.shortcuts import render_to_response


def home(request):
    context = {'page': 'home'}
    return render_to_response('home.html', context)

