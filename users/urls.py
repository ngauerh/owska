from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('register/', Register.as_view(), name='register'),  # 用户注册
    path('login/', SignIn.as_view(), name='sign_in'),  # 用户登陆
    path('loginout/', logout, name='logout'),  # 用户登出
    path('captcha/', captcha, name='captcha'),  # 验证码
    path('active/<token>/', ActiveView.as_view(), name='active'),  # 用户激活
    path('member/<username>/', member_info, name='member_info'),  # 个人主页
    path('change_avatar', ChangeAvatar.as_view(), name='change_avatar'),  # 修改头像
]
