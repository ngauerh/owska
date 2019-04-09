from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
import time
import hashlib
import random
# https://blog.csdn.net/weixin_42134789/article/details/80753051


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    f1 = str(random.randint(1, 1000)) + chr(random.randint(97, 122))
    f2 = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
    return os.path.join("avatars", f2, f1, instance.name, filename)


class User(AbstractUser):
    name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(null=True, upload_to=user_directory_path)  # 头像

    class Meta(AbstractUser.Meta):
        pass
