from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from server.models.Tweet import Tweet
import hashlib
import os


def user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    user_profile_view = False
    username = request.user.get_username()
    if not os.path.isfile('server/static/images/avatars/' + request.user.username):
        username_hash = '7d97481b1fe66f4b51db90da7e794d9f'
    else:
        username_hash = hashlib.md5(username.encode('utf-8')).hexdigest()
    tweets = None
    try:
        if request.method == "POST" and request.FILES['avatar']:
            avatar = request.FILES['avatar']
            if os.path.isfile('server/static/images/avatars/' + username_hash):
                os.remove('server/static/images/avatars/' + username_hash)
            fs = FileSystemStorage(location='server/static/images/avatars')
            fs.save(username_hash, avatar)
            return redirect('/user/')
        elif request.method == "GET" and request.path.startswith('/user/') and request.GET:
            for key, value in request.GET.items():
                tweets = Tweet.objects.filter(username=key).order_by('-date')
                for x in tweets:
                    if not os.path.isfile('server/static/images/avatars/' + x.username_hash):
                        x.username_hash = '7d97481b1fe66f4b51db90da7e794d9f'
                if not tweets:
                    raise Exception('No tweets to show')
        else:
            user_profile_view = True
    except Exception:
        user_profile_view = True
    return render(request, 'user.html',
                  {'user_profile_view': user_profile_view, 'tweets': tweets, 'username_hash': username_hash,
                   'username': username})
