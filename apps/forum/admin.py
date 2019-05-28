from django.contrib import admin

# Register your models here.

from .models import *
admin.site.site_header = "owska后台管理"
admin.site.site_title = "owska后台管理系统"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'starter', 'last_updated', 'board', 'views', 'comment_num')
    search_fields = ('title', 'starter', "board__name",)
    filter_horizontal = ('tags',)


admin.site.register(Tag)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'path', 'is_top')
