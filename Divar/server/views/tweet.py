from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from server.models.Tweet import TweetForm
import hashlib


def tweet(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == "POST":
        f = TweetForm(request.POST)
        if f.is_valid():
            f = f.save(commit=False)
            f.hashtags = hashtag_extractor(f.body)
            f.username = request.user.get_username()
            f.username_hash = hashlib.md5(f.username.encode('utf-8')).hexdigest()
            f.save()
            return redirect('/')
    else:
        f = TweetForm()
    return render(request, 'tweet.html', {'form': f})


def hashtag_extractor(text):
    text = str(text)
    text = text.replace(',', ' ').replace('.', ' ').replace('/', ' ').replace('&', ' ').replace('@', ' ')\
        .replace('\\', ' ').replace('(', ' ').replace(')', ' ').replace('*', ' ').replace('^', ' ')\
        .replace('%', ' ').replace('$', ' ').replace('!', ' ').replace('-', ' ').replace('+', ' ')\
        .replace('=', ' ').replace(']', ' ').replace('[', ' ').replace('{', ' ').replace('}', ' ')\
        .replace('\'', ' ').replace('"', ' ').replace(';', ' ').replace(':', ' ').replace('|', ' ')\
        .replace('`', ' ').replace('~', ' ').replace('<', ' ').replace('>', ' ').replace('#', ' #')

    text = text.split(' ')
    hashtags = []
    for h in text:
        if h.startswith('#') and len(h) > 1:
            hashtags.append(h)

    return ''.join(hashtags)
