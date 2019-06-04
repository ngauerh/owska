from django import template
from users.models import FollowUser, PostNumbers
from forum.models import *
import datetime
register = template.Library()


@register.simple_tag
def collect_board_count(request):
    collect_board_count = CollectedBoard.objects.filter(starter_id=request.user.id).all().count()
    return collect_board_count


@register.simple_tag
def collect_topic_count(request):
    collect_topic_count = Collected.objects.filter(starter_id=request.user.id).all().count()
    return collect_topic_count


@register.simple_tag
def follow_user_count(request):
    follow_user_count = FollowUser.objects.filter(master=request.user.id).all().count()
    return follow_user_count


@register.simple_tag
def signed_date(request):
    u = PostNumbers.objects.filter(master_id=request.user.id).first()
    if u.created_at.date() == datetime.datetime.now(datetime.timezone.utc).date():
        return False
    else:
        return True
