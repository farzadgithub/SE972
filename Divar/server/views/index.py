from django.shortcuts import render
from server.models.Tweet import Tweet
import os


def index(request):
    tweets = Tweet.objects.all().order_by('-date')
    for x in tweets:
        if not os.path.isfile('server/static/images/avatars/' + x.username_hash):
            x.username_hash = '7d97481b1fe66f4b51db90da7e794d9f'

    return render(request, 'index.html', {"tweets": tweets})
