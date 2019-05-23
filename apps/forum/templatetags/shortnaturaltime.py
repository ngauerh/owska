from django import template
import datetime
register = template.Library()


@register.filter
def shortnaturaltime(value):
    c = datetime.datetime.now(datetime.timezone.utc)-value
    if c.days:
        return str(c.days) + '天之前'
    elif c.seconds:
        if c.seconds < 60:
            return str(c.seconds) + '秒之前'
        elif 60 <= c.seconds < 3600:
            return str(c.seconds//60) + '分钟之前'
        else:
            return str(c.seconds//3600) + '小时之前'


@register.filter
def isonline(value):
    c = datetime.datetime.now(datetime.timezone.utc)-value
    if c.seconds < 120:
        return True
    else:
        return False

