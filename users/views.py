from django.shortcuts import render, redirect
from django.conf import settings
from .forms import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from .backends import send_active_email
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
import redis
import random
import io
from django.http import HttpResponse
from django.views.generic.base import View
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.hashers import make_password, check_password
from .models import *


class MyRedis(object):
    def __init__(self):
        self.r = redis.Redis(host=settings.REDIS_HOSTS, port=settings.REDIS_PORT, password=settings.REDIS_PASSWD, db=2, decode_responses=True)

    def str_get(self, k):
        res = self.r.get(k)
        if res:
            return res.decode()

    def str_set(self, k, v, time=None):
        self.r.set(k, v, time)

    def push_list(self, k, *args):
        self.r.lpush(k, args)
        self.r.expire(k, 900)

    def range_list(self, k, stime, etime):
        res = self.r.lrange(k, stime, etime)
        return res

    def del_list(self, k):
        self.r.delete(k)


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
                MyRedis().push_list(username, username)
                MyRedis().push_list(username, name)
                MyRedis().push_list(username, email)
                MyRedis().push_list(username, password)

                serializer = Serializer(settings.SECRET_KEY, 3600 * 7)
                info = {'confirm': username}
                token = serializer.dumps(info)
                token = token.decode()
                send_active_email(token, username, email)
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
            # 获取待激活用户名
            username = info['confirm']
            u.password = MyRedis().range_list(username, 0, 1)[0].lstrip("('").rstrip("',)")
            u.email = MyRedis().range_list(username, 1, 2)[0].lstrip("('").rstrip("',)")
            u.name = MyRedis().range_list(username, 2, 3)[0].lstrip("('").rstrip("',)")
            u.username = username
            # 将用户信息存入数据库
            u.save()
            # 删除token
            MyRedis().del_list(username)
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
        a = User.objects.filter(username=username)
        if a:
            pw = [i for i in a][0]
        else:
            context = {'info': '账号不存在'}
            return render(request, 'login.html', context)
        password = request.POST.get('password')
        if check_password(password, pw.password):
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            # request.session['username'] = username
            # request.session['uid'] = pw.id
            # request.session['avatar'] = str(pw.avatar)
            return redirect(reverse('forum:index'))
        else:
            context = {'info': '密码错误'}
            return render(request, 'login.html', context)


# 登出
def logout(request):
    # del request.session['username']
    # del request.session['uid']
    auth.logout(request)
    return redirect(reverse('forum:index'))


# 用户信息
def member_info(request, username):
    return render(request, 'users/member.html')


# 修改头像
class ChangeAvatar(View):
    @staticmethod
    def get(request):
        return render(request, 'users/change_info.html')

    @staticmethod
    def post(request):
        avatar = request.FILES['avatar']
        ob = User.objects.get(id=request.session['uid'])
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








