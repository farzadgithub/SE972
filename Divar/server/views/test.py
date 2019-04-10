from django.shortcuts import render, redirect
from server.models.Tweet import TweetForm


def test(request):
    if request.method == "POST":
        f = TweetForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('/')
    else:
        f = TweetForm()
    return render(request, 'test.html', {'form': f})
