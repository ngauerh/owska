from django.urls import path
from .views import *

app_name = 'forum'
urlpatterns = [
    path('', index, name='index'),  # 首页
    path('new', NewTopic.as_view(), name='new'),  # 发送新主题

]
