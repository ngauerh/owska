from django.contrib import admin

# Register your models here.

from .models import *
# https://blog.csdn.net/xyw_blog/article/details/8951808
# https://www.cnblogs.com/wumingxiaoyao/p/6928297.html
# https://www.cnblogs.com/wumingxiaoyao/p/6928297.html
admin.site.site_header = "后台管理"   # 修改登陆界面标题
admin.site.site_title = "后台管理系统"


@admin.register(Siteinfo)
class SiteinfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


@admin.register(FriendlyLink)
class FriendlyLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')





