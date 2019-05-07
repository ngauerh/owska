from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = 'forum'

router = routers.DefaultRouter()
router.register('_board', GetBoard)

urlpatterns = [
    path('', index, name='index'),  # 首页
    path('new', NewTopic.as_view(), name='new'),  # 发帖
    path('t/<str:path>/', topic, name='topic'),
    path('api', include(router.urls)),  # 全部主题

]
