# Generated by Django 2.1.8 on 2019-06-04 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190603_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='BanIP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ban_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('stop_time', models.DateTimeField(verbose_name='结束时间')),
            ],
            options={
                'verbose_name_plural': '封禁IP',
                'verbose_name': '封禁IP',
            },
        ),
        migrations.CreateModel(
            name='BanUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('stop_time', models.DateTimeField(verbose_name='结束时间')),
            ],
            options={
                'verbose_name_plural': '封禁用户',
                'verbose_name': '封禁用户',
            },
        ),
        migrations.AlterModelOptions(
            name='postnumbers',
            options={'verbose_name': '用户发帖次数', 'verbose_name_plural': '用户发帖次数'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterField(
            model_name='postnumbers',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='签到时间'),
        ),
        migrations.AddField(
            model_name='banuser',
            name='ban_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ban_user', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
