from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from server.models.Category import Subcategory, Cluster
from server.models.Post import PostForm
import hashlib


def post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == "POST":
        f = PostForm(request.POST)
        if f.is_valid():
            f = f.save(commit=False)
            f.search_keywords = search_extractor(f.body)
            f.username = request.user.get_username()
            f.username_hash = hashlib.md5(f.username.encode('utf-8')).hexdigest()
            f.save()
            return redirect('/')
    else:
        f = PostForm()
    return render(request, 'post.html', {'form': f})


def search_extractor(text):
    text = str(text)
    text = text.replace(',', ' ').replace('.', ' ').replace('/', ' ').replace('&', ' ').replace('@', ' ') \
        .replace('\\', ' ').replace('(', ' ').replace(')', ' ').replace('*', ' ').replace('^', ' ') \
        .replace('%', ' ').replace('$', ' ').replace('!', ' ').replace('-', ' ').replace('+', ' ') \
        .replace('=', ' ').replace(']', ' ').replace('[', ' ').replace('{', ' ').replace('}', ' ') \
        .replace('\'', ' ').replace('"', ' ').replace(';', ' ').replace(':', ' ').replace('|', ' ') \
        .replace('`', ' ').replace('~', ' ').replace('<', ' ').replace('>', ' ').replace('#', ' ')

    text = text.split(' ')
    keywords = []
    for h in text:
        if len(h) > 1:
            keywords.append(h)

    return ''.join(keywords)


def load_subcategories(request):
    category_id = request.GET.get('category')

    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'hr/subcategory_drop_down_list_options.html', {'subcategories': subcategories})


def load_cluster(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    clusters = Cluster.objects.filter(category_id=category_id, subcategory_id=subcategory_id).order_by('name')
    return render(request, 'hr/cluster_drop_down_list_options.html', {'clusters': clusters})
