from django.http import HttpResponseForbidden, HttpResponseRedirect

from django.contrib.sessions.models import Session

from server.api.IDS.login import login_attempt
from server.models import BlockedIP
from server.views.ids import make_a_request_detail_obj_for_response, IDS_v1, get_ip, IDS_v2


class CheckForIDSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ip = get_ip(request)
        blocked_ip = BlockedIP.objects.filter(ip=ip)
        if blocked_ip:
            return HttpResponseForbidden()

        request_detail = make_a_request_detail_obj_for_response(request)
        is_ids1 = IDS_v1(request_detail)
        is_ids2 = IDS_v2(request, request_detail)
        is_login_attempt, state, response = login_attempt(request, request_detail, response)

        if is_login_attempt and state:
            return HttpResponseRedirect('/')
        if is_ids1 or is_ids2:
            new_blocked_ip = BlockedIP(ip=ip)
            new_blocked_ip.save()
            return HttpResponseForbidden()
        return response

    def process_request(self, request):
        cur_session_key = request.user.userprofile.session_key
        if cur_session_key and cur_session_key != request.session.session_key:
            Session.objects.get(session_key=cur_session_key).delete()
        # the following can be optimized(do not save each time if value not changed)
        request.user.userprofile.session_key = request.session.session_key
        request.user.userprofile.save()
