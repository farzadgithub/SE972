from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from server.models import Userprofile
from server.models.Signup import SignupForm


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == "POST":
        f = SignupForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data['username']
            new_user = User.objects.get(username=username)
            prof = Userprofile(user=new_user)
            prof.save()
            return redirect('login')
    else:
        f = SignupForm()
    return render(request, 'registration/signup.html', {'form': f})
