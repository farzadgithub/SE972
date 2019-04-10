from django.shortcuts import render
import django.contrib.auth as dj_auth
from django.db.models import Sum
from django.contrib.auth.models import User

from server.api.IDS.email import send_email
from server.api.captcha.generate import generate
from server.api.captcha.validate import validate
from server.models import LoginForm, Userprofile, LoginAttempts
from server.models.Login import LoginFormCaptcha

FAILED_LOGIN_ATTEMPTS = 3


def login_attempt(request, request_detail, response):
    if request.path == '/login/':
        login_attempts = LoginAttempts.objects.all()
        total = login_attempts.filter(ip=request_detail.ip).aggregate(total=Sum('failed_attempts'))['total']
        if total and total > FAILED_LOGIN_ATTEMPTS:
            if request.method == "POST":
                f = LoginFormCaptcha(data=request.POST)
                if f.is_valid():
                    username = f.cleaned_data.get('username')
                    password = f.cleaned_data.get('password')
                    captcha = f.cleaned_data.get('captcha')

                    if validate(request_detail.ip, captcha):
                        user = dj_auth.authenticate(username=username, password=password)
                        if user is not None:
                            dj_auth.login(request, user)
                            send_email(user.email, 'success 2')
                            login_attempts.filter(ip=request_detail.ip, user=username).update(failed_attempts=0)
                            return True, True, response
                    fail = login_attempts.filter(ip=request_detail.ip, user=username)
                    try:
                        email = User.objects.filter(username=username).values('email')[0]['email']
                        send_email(email, 'failure 1')
                    except Exception:
                        print('oh 1')
                    if fail:
                        fail.update(failed_attempts=fail.values('failed_attempts')[0]['failed_attempts'] + 1)
                    else:
                        fail_login = LoginAttempts(ip=request_detail.ip, user=username, failed_attempts=1)
                        fail_login.save()

            f = LoginFormCaptcha()
            captcha_base64 = generate(request_detail.ip)
            return True, False, render(request, 'registration/login.html', {'form': f, 'captcha': captcha_base64})
        else:
            if request.method == "POST":
                f = LoginForm(data=request.POST)
                if f.is_valid():
                    username = f.cleaned_data.get('username')
                    password = f.cleaned_data.get('password')

                    user = dj_auth.authenticate(username=username, password=password)
                    if user is not None:
                        dj_auth.login(request, user)
                        send_email(user.email, 'success 3')
                        login_attempts.filter(ip=request_detail.ip, user=username).update(failed_attempts=0)
                        return True, True, response
                    fail = login_attempts.filter(ip=request_detail.ip, user=username)
                    try:
                        email = User.objects.filter(username=username).values('email')[0]['email']
                        send_email(email, 'failure 2')
                    except Exception:
                        print('oh 2')
                    if fail:
                        fail.update(failed_attempts=fail.values('failed_attempts')[0]['failed_attempts'] + 1)
                    else:
                        fail_login = LoginAttempts(ip=request_detail.ip, user=username, failed_attempts=1)
                        fail_login.save()
                else:
                    username = f.cleaned_data.get('username')
                    fail = login_attempts.filter(ip=request_detail.ip, user=username)
                    try:
                        email = User.objects.filter(username=username).values('email')[0]['email']
                        send_email(email, 'failure 3')
                    except Exception:
                        print('oh 3')

                    if fail:
                        fail.update(failed_attempts=fail.values('failed_attempts')[0]['failed_attempts'] + 1)
                    else:
                        fail_login = LoginAttempts(ip=request_detail.ip, user=username, failed_attempts=1)
                        fail_login.save()

            f = LoginForm()
            return True, False, render(request, 'registration/login.html', {'form': f})
    else:
        return False, False, response
