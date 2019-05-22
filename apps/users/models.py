from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
import time
import hashlib
import random


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    f1 = str(random.randint(1, 1000)) + chr(random.randint(97, 122))
    f2 = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
    return os.path.join("avatars", f2, f1, instance.name, filename)


def default_avatars():
    filename = str(random.randint(1, 10)) + '.png'
    return os.path.join('avatars/default', filename)


class User(AbstractUser):
    name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(null=True, upload_to=user_directory_path, default=default_avatars)  # 头像
    is_online = models.IntegerField('是否在线', default=0)
    website = models.URLField('个人网站', max_length=100, null=True)
    company = models.CharField('所在公司', max_length=50, null=True)
    location = models.CharField('所在地', max_length=50, null=True)
    weibo = models.CharField('微博', max_length=50, null=True)
    twitter = models.CharField('twitter', max_length=50, null=True)
    github = models.CharField('github', max_length=50, null=True)
    instagram = models.CharField('instagram', max_length=50, null=True)
    telegram = models.CharField('telegram', max_length=50, null=True)
    linkedin = models.CharField('linkedin', max_length=50, null=True)
    biography = models.TextField('个人简介', null=True)

    class Meta(AbstractUser.Meta):
        pass

