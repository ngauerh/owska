from django.db import models
from users.models import User
from django.utils.text import Truncator
from markdown import markdown
from django.utils.html import mark_safe

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

    class Meta:
        verbose_name = '板块'
        verbose_name_plural = "板块"   # 复数

    def __str__(self):
        return self.name


# 主题
class Topic(models.Model):
    """
    id, 标题，内容，发帖人，发帖时间，所属板块，标签, 阅读量, 路径
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, max_length=100, blank=True)
    views = models.PositiveIntegerField(default=0)  # 浏览量
    comment_num = models.IntegerField(default=0)  # 评论数
    path = models.CharField('路径', max_length=250, unique=True)

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = "主题"   # 复数

    def __str__(self):
        return self.title

    def get_reply_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))


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


# 评论表
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = "评论"   # 复数

    def __str__(self):
        return self.content

    def get_reply_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))


