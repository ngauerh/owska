import re
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializer import *
import json
import time
import datetime
from .forms import *
from .models import *
from users.models import User, FollowUser, PostNumbers
from pypinyin import lazy_pinyin
from django.utils.decorators import method_decorator
from .tips import message_tips


# 首页
def index(request):
    tab = request.GET.get('tab')
    board_top_list = Board.objects.filter(is_top=1).all()
    if tab:
        if tab == 'hot':
            topic_list = Topic.objects.filter(last_updated__gte=datetime.datetime.now(datetime.timezone.utc).date())\
                .select_related('starter', 'board').order_by('-comment_num')[:45]
            return render(request, 'index.html', locals())
        try:
            bid = Board.objects.get(path=tab)
            topic_list = Topic.objects.filter(board=bid.id).select_related('starter', 'board').order_by('-pk')[:45]
        except:
            topic_list = Topic.objects.select_related('starter', 'board').order_by('-pk')[:45]
    else:
        topic_list = Topic.objects.select_related('starter', 'board').order_by('-pk')[:45]

    return render(request, 'index.html', locals())


# 获取所有板块名
class GetBoard(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# 主题
def topic(request, path):
    t = Topic.objects.filter(path=path).first()
    comments = Comments.objects.filter(topic=t.id).all()
    collect = Collected.objects.filter(topic_id=t.id, starter_id=request.user.id).first()
    return render(request, 'topic/topic.html', locals())


# 板块
def board_detail(request, path):
    bid = Board.objects.get(path=path)
    contact_list = Topic.objects.filter(board=bid.id).select_related('starter', 'board').order_by('-pk')
    paginator = Paginator(contact_list, 5)

    page = request.GET.get('page')
    topic_list = paginator.get_page(page)
    board_all = contact_list.count()

    collect = CollectedBoard.objects.filter(board_id=bid.id, starter_id=request.user.id).first()
    return render(request, 'topic/board.html', locals())


# 发帖
class NewTopic(View):
    @method_decorator(login_required)
    def get(self, request):
        obj = BoardList()
        p_times = PostNumbers.objects.filter(master_id=request.user.id).first().num_times
        return render(request, 'topic/new_topic.html', locals())

    @method_decorator(login_required)
    def post(self, request):
        form = TopicForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.starter_id = User.objects.filter(id=request.user.id).first().id
            t.tags_id = 1
            t.path = '-'.join(lazy_pinyin(request.POST['title'])).replace(' ', '')
            try:
                t.save()
            except IntegrityError as e:
                t.path = '-'.join(lazy_pinyin(request.POST['title'])).replace(' ', '') + '-' + str(time.time())[:10]
                t.save()
            p = PostNumbers.objects.filter(master_id=request.user.id).first()
            p.num_times -= 1
            p.save()
            res = {"success": True, "msg": "成功"}
            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            return render(request, 'topic/new_topic.html')


# 回帖评论
class TopicComments(View):
    @method_decorator(login_required)
    def post(self, request):
        f = CommentsForm(request.POST)
        replay_user_data = request.POST['replay_user_data']
        replay_user_id = request.POST['replay_user_id']
        if f.is_valid():
            t = f.save(commit=False)
            t.author_id = request.user.id
            cc = request.POST['content']
            if cc.startswith('@'):
                _ = re.match('@(.*?) ', cc)
                c = cc.lstrip(_.group())
                t.content = replay_user_data + c
                t.replay_user_id = replay_user_id
            t.save()
            # 帖子评论数+1
            c = Topic.objects.filter(id=request.POST['topic']).first()
            c.comment_num += 1
            c.save()
            res = {"success": True, "msg": "回复成功"}

            tips_info = {
                'topic': request.POST['topic'],
                'sender': request.user.id,
                'receiver': c.starter.id,
                'tips_action': '回复',
                'tips_content': request.POST['content']
            }

            message_tips(**tips_info)
            request.session['notic_message_nums'] += '1'

            return JsonResponse(res)
        else:
            print(f.errors)


# 赞同评论
class CommentStars(View):
    @method_decorator(login_required)
    def post(self, request):
        s = Comments.objects.filter(id=request.POST['cid']).first()
        s.stars += 1
        s.save()
        res = {"success": True, "msg": "赞同回复成功"}

        tips_info = {
            'topic': s.topic.id,
            'sender': request.user.id,
            'receiver': s.topic.starter.id,
            'tips_action': '赞同',
            'tips_content': s.content,
        }

        message_tips(**tips_info)
        request.session['notic_message_nums'] += '1'

        return JsonResponse(res)


# 收藏主题
class CollectTopic(View):
    @method_decorator(login_required)
    def get(self, request):
        get_collect_topic = Collected.objects.filter(starter_id=request.user.id).all().order_by('-pk')
        paginator = Paginator(get_collect_topic, 5)

        page = request.GET.get('page')
        topic_list = paginator.get_page(page)
        board_all = get_collect_topic.count()
        return render(request, 'users/collect_topic.html', locals())

    @method_decorator(login_required)
    def post(self, request):
        try:
            s = Collected()
            s.starter_id = request.user.id
            s.topic_id = request.POST['collect']
            s.save()
            res = {"success": True, "msg": "收藏成功"}

            t = Topic.objects.filter(id=request.POST['collect']).first()
            tips_info = {
                'topic': t.id,
                'sender': request.user.id,
                'receiver': t.starter.id,
                'tips_action': '收藏',
                'tips_content': t.title,
            }

            message_tips(**tips_info)
            request.session['notic_message_nums'] += '1'

            return JsonResponse(res)
        except:
            res = {"success": False, "msg": "不好意思，发生未知错误"}
            return JsonResponse(res)


# 取消主题收藏
class UnCollectTopic(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            Collected.objects.filter(topic_id=request.POST['collect'], starter_id=request.user.id).first().delete()
            res = {"success": True, "msg": "取消收藏成功"}
            return JsonResponse(res)
        except:
            res = {"success": False, "msg": "不好意思，发生未知错误"}
            return JsonResponse(res)


# 收藏板块
class CollectBoard(View):
    @method_decorator(login_required)
    def get(self, request):
        get_collect_board = CollectedBoard.objects.filter(starter_id=request.user.id).all()
        return render(request, 'users/collect_board.html', locals())

    @method_decorator(login_required)
    def post(self, request):
        try:
            s = CollectedBoard()
            s.starter_id = request.user.id
            s.board_id = request.POST['collect']
            s.save()
            res = {"success": True, "msg": "收藏成功"}
            return JsonResponse(res)
        except:
            res = {"success": False, "msg": "不好意思，发生未知错误"}
            return JsonResponse(res)


# 取消板块收藏
class UnCollectBoard(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            CollectedBoard.objects.filter(board_id=request.POST['collect'], starter_id=request.user.id).first().delete()
            res = {"success": True, "msg": "取消收藏成功"}
            return JsonResponse(res)
        except:
            res = {"success": False, "msg": "不好意思，发生未知错误"}
            return JsonResponse(res)


# 消息提醒
class NoticeMessage(View):
    @method_decorator(login_required)
    def get(self, request):
        request.session['notic_message_nums'] = ''
        m_list = MessageTips.objects.filter(receiver_id=request.user.id).all().order_by('-pk')
        paginator = Paginator(m_list, 2)

        page = request.GET.get('page')
        message_list = paginator.get_page(page)
        return render(request, 'topic/tips.html', locals())
