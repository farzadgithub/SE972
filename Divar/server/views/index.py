from django.shortcuts import render
from server.models.Post import Post
import os


def index(request):
    posts = Post.objects.all().order_by('-date')
    for x in posts:
        if not os.path.isfile('server/static/images/avatars/' + x.username_hash):
            x.username_hash = '7d97481b1fe66f4b51db90da7e794d9f'

    return render(request, 'index.html', {"posts": posts})
