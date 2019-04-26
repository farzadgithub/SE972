import datetime
import json
import re

from django.contrib.auth.models import User
from django.utils import timezone

from server.models import LoginForm, Userprofile
from server.models.RequestDetail import RequestDetail

h = datetime.timedelta(seconds=2)
n = 40


def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""

    return ip


def get_browser(request):
    try:
        browser = request.META['HTTP_USER_AGENT']
    except:
        browser = ""
    return browser


def make_a_request_detail_obj_for_response(request):
    try:
        ip = get_ip(request)
        time = timezone.now()
        browser = get_browser(request)
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            username = request.user.get_username()
        else:
            username = ''

        request_detail = RequestDetail(ip=ip, time=time, browser=browser, is_authenticated=is_authenticated,
                                       username=username)
        request_detail.save()
        return request_detail
    except Exception as e:
        print("PROBLEM IN MAKING DETAILS!", e)


def IDS_v1(request_detail):
    ip = request_detail.ip
    browser = request_detail.browser

    last_details = RequestDetail.objects.filter(ip=ip).order_by('-time')[:n]
    # last_details = filter(myFunc, list(RequestDetail.objects.all))
    is_ids = False
    number = last_details.__sizeof__()
    last_details = list(last_details)
    if number < n:
        return is_ids
    #     for to find if two elements occurence time delta is less than h
    number_of_doubtful_requests = 0
    for i in range(len(last_details)):
        if i != len(last_details):
            y = (last_details[i - 1].time - last_details[i].time)
            if y <= h:
                number_of_doubtful_requests += 1
                if number_of_doubtful_requests >= n:
                    is_ids = True
                    break
            else:
                break
    return is_ids


EXEMPT_URLS = [re.compile(r'^login$')]


def IDS_v2(request, request_detail):
    path = request.path_info.lstrip('/')
    if not request_detail.is_authenticated:
        if not any(url.match(path) for url in EXEMPT_URLS):
            request_detail.is_authenticated = False
            request_detail.save()
        else:
            if EXEMPT_URLS[0].match(path):
                if request.method == "POST":
                    f = LoginForm(data=request.POST)
                    if f.is_valid():
                        username = f.cleaned_data.get('username')
                        password = f.cleaned_data.get('password')
                        user = User.objects.get(username=username)
                        if not user.check_password(password):
                            request_detail.is_authenticated = False
                            request_detail.save()
                        if user is None:
                            request_detail.is_authenticated = False
                            request_detail.save()

            elif EXEMPT_URLS[1].match(path) or EXEMPT_URLS[2].match(path):
                try:
                    data = json.loads(request.body)
                    key = data['authentication_key']
                    userprofile = Userprofile.objects.get(authentication_key=key)
                    if userprofile is None:
                        request_detail.is_authenticated = False
                        request_detail.save()

                except:
                    request_detail.is_authenticated = False
                    request_detail.save()

    ip = request_detail.ip
    last_details = RequestDetail.objects.filter(ip=ip).order_by('-time')[:n]
    is_ids = False
    number = last_details.__sizeof__()
    last_details = list(last_details)
    if number < n:
        return is_ids

    is_ids = True
    for i in range(0, n, 1):
        if last_details[i].is_authenticated:
            is_ids = False

    return is_ids


# Allow only one concurrent login per user in django app [duplicate]
