from django import template
from users.models import FollowUser
from forum.models import *
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
