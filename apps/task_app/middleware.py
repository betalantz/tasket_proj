from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

import pytz
from ..user_app.models import User
from ..user_app.views import sessionCheck


class TimezoneMiddleware(MiddlewareMixin):
    # def __init__(self, get_response):
    #     self.get_response = get_response

    # def __call__(self, request):
    #     if (request.session['auth_id']):
    #         currTZ = User.objects.get(id=request.session['auth_id']).timezone
    #         print currTZ
    #         timezone.activate(pytz.timezone(currTZ))
    #     else:
    #         timezone.deactivate()
    #     return self.get_response(request)

    def process_request(self, request):
        if sessionCheck(request):
            currTZ = User.objects.get(id=request.session['auth_id']).timezone
            print currTZ
            timezone.activate(pytz.timezone(currTZ))
        else:
            timezone.deactivate()