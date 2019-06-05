from django.db import models
from users.models import User
from markdown import markdown
from django.utils.html import mark_safe
from django.utils.html import format_html


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
    name = models.CharField('名称', max_length=30, unique=True)  # 板块名
    description = models.CharField('简介', max_length=100)  # 简介
    path = models.CharField('路径', max_length=100)  # 板块url
    icon = models.ImageField('图标', null=True, upload_to='icon/board')
    is_top = models.BooleanField('是否出现在导航栏', default=False)

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
    title = models.CharField('标题', max_length=255)
    content = models.TextField('内容')
    starter = models.ForeignKey(User, related_name='topics', verbose_name='发帖人', on_delete=models.CASCADE)
    last_updated = models.DateTimeField('更新时间', auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', verbose_name='节点', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', max_length=100, blank=True)
    views = models.PositiveIntegerField('浏览量', default=0)  # 浏览量
    comment_num = models.IntegerField('评论数', default=0)  # 评论数
    path = models.CharField('路径', max_length=250, unique=True)
    ban_comments = models.BooleanField('是否允许回复', default=True)

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = "主题"

    def __str__(self):
        return self.title

    def get_reply_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def ban_comments_status(self):
        if self.ban_comments:
            color_code = 'green'
            status = '允许'
        else:
            color_code = 'red'
            status = '禁止'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            status
        )

    ban_comments_status.short_description = u"禁止回复"


# 回复表
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='主题',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='回复者',  related_name='comment_user')
    content = models.TextField(blank=False)
    stars = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    replay_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='回复对象', related_name='replay_user',
                                    null=True, blank=True)

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = "回复"

    def __str__(self):
        return self.content[0:100]

    def get_reply_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def short_content(self):
        if len(str(self.content)) > 100:
            return '{}...'.format(str(self.content)[0:100])
        else:
            return str(self.content)

    short_content.allow_tags = True


# 用户收藏
class Collected(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    starter = models.ForeignKey(User, on_delete=models.CASCADE)


# 板块收藏
class CollectedBoard(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    starter = models.ForeignKey(User, on_delete=models.CASCADE)



