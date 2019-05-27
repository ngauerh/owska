from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = 'forum'

router = routers.DefaultRouter()
router.register('_board', GetBoard)

urlpatterns = [
    path('', index, name='index'),  # 首页
    path('new', NewTopic.as_view(), name='new'),  # 发帖
    path('t/<str:path>/', topic, name='topic'),  # 主题帖
    path('b/<str:path>/', board_detail, name='board'),  # 板块
    path('api', include(router.urls)),  # 全部主题
    path('comment', TopicComments.as_view(), name='comments'),
    path('comment_stars', CommentStars.as_view(), name='cstars'),  # 赞同评论
    path('topic_collect', CollectTopic.as_view(), name='topic_collect'),  # 主题收藏
    path('topic_uncollect', UnCollectTopic.as_view(), name='topic_uncollect'),  # 取消收藏
    path('board_collect', CollectBoard.as_view(), name='board_collect'),  # 节点收藏
    path('board_uncollect', UnCollectBoard.as_view(), name='board_uncollect'),  # 取消收藏
]
