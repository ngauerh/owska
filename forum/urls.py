from django.urls import path
from .views import *

app_name = 'forum'
urlpatterns = [
    path('', index, name='index'),  # 用户注册

]
