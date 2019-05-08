from django.db import IntegrityError
from django.http import HttpResponse
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
    return render(request, 'topic/topic.html', locals())


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
            res = {"success": True, "msg": "成功"}
            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            print(f.errors)



