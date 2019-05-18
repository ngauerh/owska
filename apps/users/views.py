from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from .backends import OwskaEmail
from django.urls import reverse
from django.contrib import auth
import redis
from django.contrib.auth.decorators import login_required
import io
from django.http import HttpResponse
from django.views.generic.base import View
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from forum.models import Topic, Comments, Collected


class MyRedis(object):
    def __init__(self):
        self.r = redis.Redis(host=settings.REDIS_HOSTS, port=settings.REDIS_PORT, password=settings.REDIS_PASSWD, db=2, decode_responses=True)

    def str_get(self, k):
        res = self.r.get(k)
        if res:
            return res.decode()

    def str_set(self, k, v, time=None):
        self.r.set(k, v, time)

    def push_list(self, k, v):
        self.r.lpush(k, v)
        self.r.expire(k, 900)

    def range_list(self, k, stime, etime):
        res = self.r.lrange(k, stime, etime)
        return res

    def del_list(self, k):
        self.r.delete(k)

    def make_hash(self, name, key, value):
        self.r.hset(name=name, key=key, value=value)

    def del_hash(self, name):
        self.r.delete(name)


# 注册
class Register(View):
    @staticmethod
    def get(request):
        return render(request, 'register.html')

    @staticmethod
    def post(request):
        user = User.objects.all()
        verify_code = request.session['verify_code']
        if verify_code != request.POST['captcha'].lower():
            context = {'info': '验证码错误！'}
            return render(request, 'register.html', context)
        form = RegisterForm(request.POST)
        # 验证数据的合法性, 保存数据库
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password = make_password(password)
            name = request.POST.get('name')
            if user.filter(email=email):
                context = {'info': '邮箱已存在'}
                return render(request, 'register.html', context)
            else:
                MyRedis().push_list(email, username)
                MyRedis().push_list(email, name)
                MyRedis().push_list(email, email)
                MyRedis().push_list(email, password)

                serializer = Serializer(settings.SECRET_KEY, 3600 * 7)
                info = {'confirm': email}
                token = serializer.dumps(info)
                token = token.decode()
                OwskaEmail(token, username, email).send_active_email()
                context = {'info': '注册链接已发往{},请赶快前往激活'.format(email)}
                return render(request, 'info.html', context)
        else:
            context = {'info': '用户名已存在'}
            return render(request, 'register.html', context)


# 激活
class ActiveView(View):
    @staticmethod
    def get(request, token):
        """激活"""
        serializer = Serializer(settings.SECRET_KEY, 3600 * 7)
        try:
            # 解密
            u = User()
            info = serializer.loads(token)
            # 获取待激活用户邮箱
            email = info['confirm']
            u.password = MyRedis().range_list(email, 0, 1)[0].lstrip("('").rstrip("',)")
            u.email = MyRedis().range_list(email, 1, 2)[0].lstrip("('").rstrip("',)")
            u.name = MyRedis().range_list(email, 2, 3)[0].lstrip("('").rstrip("',)")
            u.username = MyRedis().range_list(email, 3, 4)[0].lstrip("('").rstrip("',)")
            # 将用户信息存入数据库
            u.save()
            # 删除token
            MyRedis().del_list(email)
            context = {'info': "激活成功"}
            return render(request, 'info.html', context)
        except:
            return HttpResponse('激活链接已失效')


# 登陆
class SignIn(View):
    @staticmethod
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        username = request.POST.get('username')
        pw = User.objects.filter(username=username).first()
        if not pw:
            context = {'info': '账号不存在'}
            return render(request, 'login.html', context)
        else:
            password = request.POST.get('password')
        if check_password(password, pw.password):
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(reverse('forum:index'))
        else:
            context = {'info': '密码错误'}
            return render(request, 'login.html', context)


# 忘记密码
class ForgetPassword(View):
    @staticmethod
    def get(request):
        return render(request, 'forget.html')

    @staticmethod
    def post(request):
        serializer = Serializer(settings.SECRET_KEY, 3600 * 7)
        email = request.POST.get('email')
        username = User.objects.filter(email=email)
        if not username:
            context = {'info': '邮箱不存在'}
            return render(request, 'forget.html', context)
        else:
            info = {'forgetpassword': email}
            token = serializer.dumps(info)
            token = token.decode()
            OwskaEmail(token, username.first().username, email).send_forget_email()
            MyRedis().push_list('forget_{}'.format(email), token)
            context = {'info': '重置密码链接已发往{},请赶快重置密码'.format(email)}
            return render(request, 'info.html', context)


# 重置密码
class ResetPassword(View):
    @staticmethod
    def get(request, token):
        context = {'res': token}
        return render(request, 'reset.html', context)

    @staticmethod
    def post(request, token):
        """重置密码"""
        serializer = Serializer(settings.SECRET_KEY, 3600 * 7)
        try:
            info = serializer.loads(token)
            # 判断用户提交的token是否被篡改
            email = info['forgetpassword']
            redis_info = MyRedis().range_list('forget_{}'.format(email), 0, 1)[0].lstrip("('").rstrip("',)")
            if token != redis_info:
                context = {'info': '重置密码出错，请重试'}
                return render(request, 'info.html', context)
            u = User.objects.filter(email=email).first()
            u.password = make_password(request.POST.get('password'))
            u.save()
            # 删除token
            MyRedis().del_list('forget_{}'.format(email))
            context = {'info': "重置密码成功，请重新登陆"}
            return render(request, 'info.html', context)
        except:
            return HttpResponse('重置密码出错，请重试')


# 登出
@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('forum:index'))


# 用户信息
@login_required
def member_info(request, username):
    user_info = User.objects.filter(username=username).first()
    topic_all = Topic.objects.filter(starter=user_info.id).order_by('-pk')

    paginator = Paginator(topic_all, 5)
    page = request.GET.get('page')
    topic_list = paginator.get_page(page)

    topic_sum = topic_all.count()
    return render(request, 'users/member.html', locals())


def member_comments(request, username):
    user_info = User.objects.filter(username=username).first()
    comments_all = Comments.objects.filter(author=user_info.id).order_by('-pk')

    paginator = Paginator(comments_all, 5)
    page = request.GET.get('page')
    comments_list = paginator.get_page(page)

    comments_sum = comments_all.count()
    return render(request, 'users/comments.html', locals())


def member_collected(request, username):
    user_info = User.objects.filter(username=username).first()
    collect_all = Collected.objects.filter(starter_id=user_info.id).order_by('-pk')

    paginator = Paginator(collect_all, 5)
    page = request.GET.get('page')
    collect_list = paginator.get_page(page)

    collect_sum = collect_all.count()

    return render(request, 'users/collected.html', locals())


def member_details(request, username):
    user_info = User.objects.filter(username=username).first()
    return render(request, 'users/details.html', locals())


# 修改头像
class ChangeAvatar(View):
    @staticmethod
    @login_required
    def get(request):
        return render(request, 'users/change_info.html')

    @staticmethod
    @login_required
    def post(request):
        avatar = request.FILES['avatar']
        ob = User.objects.get(id=request.user.id)
        ob.avatar = avatar
        ob.save()
        crop_image(os.path.join('media', str(ob.avatar)))
        request.session['avatar'] = str(ob.avatar)
        return redirect(reverse('forum:index'))


# 裁剪图片
def crop_image(file):
    img = Image.open(file)
    crop_im = img.crop((50, 50, 300, 300)).resize((200, 200), Image.ANTIALIAS)
    crop_im.save(file)
    return file


# 验证码
def captcha(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    # bgcolor = (150, 154, 194)
    width = 120
    height = 30
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点

    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    str1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZasdfghjklmnopqrstuvw'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('static/fonts/STXIHEI.TTF', 23)
    # font = ImageFont.load_default().font
    for i in range(0, 4):
        # 构造字体颜色
        fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        # 绘制4个字
        draw.text((5 + i * 24, -4), rand_str[i], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verify_code'] = rand_str.lower()
    # 内存文件操作
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')








