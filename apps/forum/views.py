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
from pypinyin import lazy_pinyin, Style


# 首页
def index(requests):
    topic_list = Topic.objects.select_related('starter', 'board').order_by('-pk')[:45]
    return render(requests, 'index.html', locals())


# 获取所有板块名
class GetBoard(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# 帖子
def topic(requests, path):
    t = Topic.objects.filter(path=path).first()
    return render(requests, 'topic/topic.html', locals())


# 发帖
class NewTopic(View):
    @staticmethod
    @login_required
    def get(request):
        obj = BoardList()
        return render(request, 'topic/new_topic.html', {"obj": obj})

    @staticmethod
    @login_required
    def post(request):
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



