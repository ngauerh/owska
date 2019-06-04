import datetime

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from users.models import BanUser, BanIP


class BanSomethingMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        i = BanIP.objects.filter(ban_ip=ip)
        if i:
            if i.first().stop_time > datetime.datetime.now(datetime.timezone.utc):
                return HttpResponse('<h3>您的ip于{}到{}之间被禁止使用</h3>'.format(str(i.first().start_time), str(i.first().stop_time)))

        b = BanUser.objects.filter(ban_user_id=request.user.id)
        if b:
            if b.first().stop_time > datetime.datetime.now(datetime.timezone.utc):
                return HttpResponse('<h3>您的账户于{}到{}之间被禁止使用</h3>'.format(str(b.first().start_time), str(b.first().stop_time)))
