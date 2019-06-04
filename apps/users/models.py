import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
import time
import hashlib
import random
from django.utils.html import format_html


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    f1 = str(random.randint(1, 1000)) + chr(random.randint(97, 122))
    f2 = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
    return os.path.join("avatars", f2, f1, instance.name, filename)


def default_avatars():
    filename = str(random.randint(0, 10)) + '.png'
    return os.path.join('avatars/default', filename)


class User(AbstractUser):
    name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(null=True, upload_to=user_directory_path, default=default_avatars)  # 头像
    is_online = models.IntegerField('是否在线', default=0)
    last_activity = models.DateTimeField('最后访问时间', auto_now_add=True, null=True, blank=True)
    activity_ip = models.GenericIPAddressField('ip地址', null=True, blank=True)
    website = models.URLField('个人网站', max_length=100, null=True, blank=True)
    company = models.CharField('所在公司', max_length=50, null=True, blank=True)
    location = models.CharField('所在地', max_length=50, null=True, blank=True)
    weibo = models.CharField('微博', max_length=50, null=True, blank=True)
    twitter = models.CharField('twitter', max_length=50, null=True, blank=True)
    github = models.CharField('github', max_length=50, null=True, blank=True)
    instagram = models.CharField('instagram', max_length=50, null=True, blank=True)
    telegram = models.CharField('telegram', max_length=50, null=True, blank=True)
    linkedin = models.CharField('linkedin', max_length=50, null=True, blank=True)
    biography = models.TextField('个人简介', null=True, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        verbose_name_plural = "用户"   # 复数


# 关注用户
class FollowUser(models.Model):
    id = models.AutoField(primary_key=True)
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_master')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')


# 拉黑用户
class BlockUser(models.Model):
    id = models.AutoField(primary_key=True)
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block_master')
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')


# 默认发帖次数
class PostNumbers(models.Model):
    id = models.AutoField(primary_key=True)
    master = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='user_post_times')
    num_times = models.IntegerField('发帖次数', default=5, null=True, blank=True)
    created_at = models.DateTimeField('签到时间', auto_now_add=True)  # 创建时间

    def signed_status(self):
        if self.created_at.date() == datetime.datetime.now(datetime.timezone.utc).date():
            color_code = 'green'
            status = '今日已签到'
        else:
            color_code = 'grey'
            status = '今日未签到'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            status
        )

    signed_status.short_description = u"签到"

    class Meta:
        verbose_name = '用户发帖次数'
        verbose_name_plural = "用户发帖次数"   # 复数


# ban用户
class BanUser(models.Model):
    id = models.AutoField(primary_key=True)
    ban_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='ban_user')
    start_time = models.DateTimeField('开始时间')
    stop_time = models.DateTimeField('结束时间')

    def ban_status(self):
        if self.start_time < datetime.datetime.now(datetime.timezone.utc) < self.stop_time:
            color_code = 'red'
            status = '正在封禁中'
        elif self.start_time > datetime.datetime.now(datetime.timezone.utc):
            color_code = 'yellow'
            status = '封禁还未开始'
        elif self.stop_time < datetime.datetime.now(datetime.timezone.utc):
            color_code = 'green'
            status = '封禁已结束'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            status
        )

    ban_status.short_description = u"封禁状态"

    class Meta:
        verbose_name = '封禁用户'
        verbose_name_plural = "封禁用户"   # 复数


# ban ip地址
class BanIP(models.Model):
    id = models.AutoField(primary_key=True)
    ban_ip = models.GenericIPAddressField('IP地址', null=True, blank=True)
    start_time = models.DateTimeField('开始时间')
    stop_time = models.DateTimeField('结束时间')

    def ban_status(self):
        if self.start_time < datetime.datetime.now(datetime.timezone.utc) < self.stop_time:
            color_code = 'red'
            status = '正在封禁中'
        elif self.start_time > datetime.datetime.now(datetime.timezone.utc):
            color_code = 'yellow'
            status = '封禁还未开始'
        elif self.stop_time < datetime.datetime.now(datetime.timezone.utc):
            color_code = 'green'
            status = '封禁已结束'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            status
        )

    ban_status.short_description = u"封禁状态"

    class Meta:
        verbose_name = '封禁IP'
        verbose_name_plural = "封禁IP"   # 复数

