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
    path('member/<username>/comments/', member_comments, name='member_comments'),
    path('member/<username>/collected/', member_collected, name='member_collected'),  # 个人收藏
    path('member/<username>/details/', MemberDetails.as_view(), name='member_details'),  # 个人信息
    path('follow/', FollowingUser.as_view(), name='follow_user'),  # 关注
    path('unfollow/', UnFollowUser.as_view(), name='unfollow'),  # 取消关注
    path('block/', BlockingUser.as_view(), name='block_user'),  # 拉黑
    path('unblock/', UnBlockUser.as_view(), name='unblock'),  # 解除拉黑
    path('change_avatar', ChangeAvatar.as_view(), name='change_avatar'),  # 修改头像
    path('forget/', ForgetPassword.as_view(), name='forget'),  # 忘记密码
    path('reset/<token>/', ResetPassword.as_view(), name='reset'),  # 重置密码
]
