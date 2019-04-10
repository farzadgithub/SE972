import django.contrib.auth as dj_auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from server.api.IDS.email import send_email
from server.models.Login import LoginForm


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == "POST":
        f = LoginForm(data=request.POST)
        if f.is_valid():
            username = f.cleaned_data.get('username')
            password = f.cleaned_data.get('password')
            user = dj_auth.authenticate(username=username, password=password)
            if user is not None:
                dj_auth.login(request, user)
                send_email(user.email, 'success 1')
                return HttpResponseRedirect('/')
    else:
        f = LoginForm()
    return render(request, 'registration/login.html', {'form': f})
