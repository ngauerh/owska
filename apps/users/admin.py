from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'activity_ip')
    search_fields = ('username', 'email', "name", 'activity_ip')
    list_per_page = 50
    ordering = ('-last_login',)


@admin.register(BanUser)
class BanUserAdmin(admin.ModelAdmin):
    list_display = ('ban_user', 'start_time', 'stop_time', 'ban_status')
    search_fields = ('ban_user__username', 'start_time', "stop_time")
    list_per_page = 50
    raw_id_fields = ("ban_user",)
    ordering = ('-stop_time',)


@admin.register(BanIP)
class BanIPAdmin(admin.ModelAdmin):
    list_display = ('ban_ip', 'start_time', 'stop_time', 'ban_status')
    search_fields = ('ban_ip', 'start_time', "stop_time",)
    list_per_page = 50
    ordering = ('-stop_time',)


@admin.register(PostNumbers)
class PostNumbersAdmin(admin.ModelAdmin):
    list_display = ('master', 'num_times', 'signed_status')
    search_fields = ('master', 'num_times', 'signed_status')
    list_per_page = 50
