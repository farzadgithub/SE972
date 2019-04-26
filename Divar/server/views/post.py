from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from server.models.Post import PostForm
import hashlib


def post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == "POST":
        f = PostForm(request.POST)
        if f.is_valid():
            f = f.save(commit=False)
            f.hashtags = hashtag_extractor(f.body)
            f.username = request.user.get_username()
            f.username_hash = hashlib.md5(f.username.encode('utf-8')).hexdigest()
            f.save()
            return redirect('/')
    else:
        f = PostForm()
    return render(request, 'post.html', {'form': f})


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
