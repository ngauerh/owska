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
from .forms import *
from .models import *
from users.models import User
from pypinyin import lazy_pinyin
from django.utils.decorators import method_decorator


# 首页
def index(request):
    tab = request.GET.get('tab')
    if tab:
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


# 帖子
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
    return render(request, 'topic/board.html', locals())


# 发帖
class NewTopic(View):
    @method_decorator(login_required)
    def get(self, request):
        obj = BoardList()
        return render(request, 'topic/new_topic.html', {"obj": obj})

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
            res = {"success": True, "msg": "成功"}
            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            print(form.errors)
            return render(request, 'topic/new_topic.html')


class TopicComments(View):
    @method_decorator(login_required)
    def post(self, request):
        f = CommentsForm(request.POST)
        if f.is_valid():
            t = f.save(commit=False)
            t.author_id = request.user.id
            t.save()
            # 帖子评论数+1
            c = Topic.objects.filter(id=request.POST['topic']).first()
            c.comment_num += 1
            c.save()
            res = {"success": True, "msg": "回复失败"}
            return JsonResponse(res)
        else:
            print(f.errors)


class CommentStars(View):
    @method_decorator(login_required)
    def post(self, request):
        s = Comments.objects.filter(id=request.POST['cid']).first()
        s.stars += 1
        s.save()
        res = {"success": True, "msg": "赞同回复失败"}
        return JsonResponse(res)


# 收藏主题
class CollectTopic(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            s = Collected()
            s.starter_id = request.user.id
            s.topic_id = request.POST['collect']
            s.save()
            res = {"success": True, "msg": "收藏成功"}
            return JsonResponse(res)
        except:
            res = {"success": False, "msg": "不好意思，发生未知错误"}
            return JsonResponse(res)


# 取消收藏
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


# 取消收藏
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
