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
        title = request.POST['title']
        content = request.POST['detail']
        starter = request.POST['starter']
        board = request.POST['board']
        view = 0
        if True:
            res = {"success": True, "msg": "发送成功"}
        else:
            res = {"success": False, "msg": "发送失败"}

        return HttpResponse(json.dumps(res), content_type="application/json")



# 节点
def boardlist(request):
    board = Board.objects.all()
    print(board)