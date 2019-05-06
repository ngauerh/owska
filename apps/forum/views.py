from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializer import *
import json
from .forms import *
from .models import *
from users.models import User


def index(requests):
    topic = Topic.objects.order_by('-pk')[:45]
    return render(requests, 'index.html', {'topic_list': topic})


# 获取所有板块名
class GetBoard(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# 发帖
class NewTopic(View):
    @staticmethod
    @login_required
    def get(request):
        return render(request, 'topic/new_topic.html',)

    @staticmethod
    @login_required
    def post(request):
        form = TopicForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.starter_id = User.objects.filter(id=request.user.id).first().id
            t.tags_id = 1
            t.save()
            res = {"success": True, "msg": "成功"}
            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            print(form.errors)
            return render(request, 'topic/new_topic.html')


