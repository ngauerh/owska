from django.db import models
from users.models import User
from django.utils.text import Truncator


# https://blog.csdn.net/devil_2009/article/details/41735611


# 标签
class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"   # 复数


# 板块
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)  # 板块名
    description = models.CharField(max_length=100)  # 简介
    path = models.CharField(max_length=100)  # 板块url

    def __str__(self):
        return self.name


# 主题
class Topic(models.Model):
    """
    id, 标题，内容，发帖人，发帖时间，所属板块，标签
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag, max_length=100, blank=True)
    views = models.PositiveIntegerField(default=0)  # 浏览量

    def __str__(self):
        return self.subject


# 帖子
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(blank=False)  # 内容
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)  # 所属主题
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # 发帖人

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)



