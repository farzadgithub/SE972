import json
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from server.api.IDS.email import send_email
from server.api.v1.tools import id_generator
from server.models import LoginAttempts
from server.views.ids import make_a_request_detail_obj_for_response

FAILED_LOGIN_ATTEMPTS = 15


@csrf_exempt
def login(request):
    key = id_generator()
    response_data = {
        'authentication_key': key
    }

    try:
        data = json.loads(request.body)
        username = data['username']
        psw = data['password']

        login_attempts = LoginAttempts.objects.all()
        request_detail = make_a_request_detail_obj_for_response(request)
        total = login_attempts.filter(ip=request_detail.ip).aggregate(total=Sum('failed_attempts'))['total']

        if total and total > FAILED_LOGIN_ATTEMPTS:
            return HttpResponse("Request Blocked")
        fail = login_attempts.filter(ip=request_detail.ip, user=username)
        try:
            email = User.objects.filter(username=username).values('email')[0]['email']
            send_email(email, 'failure 4')
        except Exception:
            print('oh')
        if fail:
            fail.update(failed_attempts=fail.values('failed_attempts')[0]['failed_attempts'] + 1)
        else:
            fail_login = LoginAttempts(ip=request_detail.ip, user=username, failed_attempts=1)
            fail_login.save()

        user = User.objects.get(username=username)
        if not user.check_password(psw):
            raise Exception('Wrong password')
        user.userprofile.authentication_key = key

        user.userprofile.save()
        return JsonResponse(response_data)

    except Exception as e:
        print(e)
        return HttpResponse("Malformed data!")
