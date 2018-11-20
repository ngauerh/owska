from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
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
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'topic/new_topic.html')
