from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
import json
from .models import *
from .forms import *
# Create your views here.


def index(requests):
    return render(requests, 'index.html')


# 发帖
class NewTopic(View):
    @staticmethod
    @login_required
    def get(request):
        return render(request, 'topic/new_topic.html')

    @staticmethod
    @login_required
    def post(request):
        # print(request.POST['detail'])
        print(request.POST['title'])
        res = {"success": True, "msg": "成功"}
        return HttpResponse(json.dumps(res), content_type="application/json")
        # form = TopicForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     res = {"success": True, "msg": "成功"}
        #     return HttpResponse(json.dumps(res), content_type="application/json")
        # return render(request, 'topic/new_topic.html')


# 节点
def boardlist(request):
    board = Board.objects.all()
    print(board)