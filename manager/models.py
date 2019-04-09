from django.db import models

# Create your models here.


class FriendlyLink(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('标题', max_length=30)
    url = models.URLField('链接')
    message = models.TextField('备注', blank=True)
    create_at = models.DateTimeField('添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'


class Siteinfo(models.Model):
    title = models.CharField('网站标题', max_length=30)
    icon = models.ImageField('网站图标', upload_to='icon')
    url = models.URLField('网站url', max_length=120)
    description = models.TextField('网站简介', blank=True)
    privacy_policy = models.TextField('隐私政策', blank=True)
    terms_of_service = models.TextField('服务条款', blank=True)

    class Meta:
        verbose_name = '网站信息'
        verbose_name_plural = '网站信息'
