from datetime import timedelta as td

from django.core.cache import cache
from users.models import User
from dateutil.parser import parse
import datetime


def last_user_activity_middleware(get_response):
    def middleware(request):

        # 获取ip
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        # 获取最后登陆时间

        key = "{}_last-activity".format(request.user.username)

        online_key = "user_online_id_{}".format(request.user.username)

        if request.user.is_authenticated:

            # 获取到上一次记录的时间
            last_activity = request.session.get(key)

            too_old_time = datetime.datetime.now(datetime.timezone.utc) - td(seconds=1)

            if not last_activity or parse(last_activity) < too_old_time:
                u = User.objects.filter(id=request.user.id)
                u.update(last_activity=datetime.datetime.now(datetime.timezone.utc))
                if request.user.activity_ip != ip:
                    u.update(activity_ip=ip)

            # 更新访问时间
            request.session[key] = datetime.datetime.now(datetime.timezone.utc).isoformat()

            cache.set(online_key, 'online', timeout=120)
            request.online_member_count = len(cache.keys("user_online_id_*"))

            request.current_visitor_ip = ip

        response = get_response(request)
        return response

    return middleware

