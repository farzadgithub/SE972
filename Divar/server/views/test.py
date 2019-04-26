from django.shortcuts import render, redirect
from server.models.Post import PostForm


def test(request):
    if request.method == "POST":
        f = PostForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('/')
    else:
        f = PostForm()
    return render(request, 'test.html', {'form': f})
