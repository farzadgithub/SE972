from server.api.v1.tools import id_generator
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse


def authentication(request):
    key = id_generator()
    response_data = {
        'authentication_key': key
    }

    try:
        username = request.user.username
        user = User.objects.get(username=username)

        user.userprofile.authentication_key = key
        user.userprofile.save()
        return JsonResponse(response_data)
    except Exception:
        return HttpResponse("Malformed data!")
