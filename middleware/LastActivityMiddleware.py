from datetime import timedelta as td
from django.utils import timezone
from django.conf import settings
from users.models import User
import datetime


def last_user_activity_middleware(get_response):
    def middleware(request):

        response = get_response(request)

        key = "last-activity"

        if request.user.is_authenticated:
            request.session[key] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            last_activity = request.session.get(key)
            print(last_activity)
            print(datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S %Z'))
            print(type(last_activity))
            too_old_time = timezone.now() - td(seconds=1)
            if not last_activity or datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S') < too_old_time:
                print('if')
            else:
                print('else')
                User.objects.filter(email=request.user).update(
                    is_online=1)


        return response

    return middleware

