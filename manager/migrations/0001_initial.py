# Generated by Django 2.1.4 on 2019-04-09 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendlyLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('url', models.URLField(verbose_name='链接')),
                ('message', models.TextField(blank=True, verbose_name='备注')),
                ('create_at', models.DateTimeField(verbose_name='添加时间')),
            ],
            options={
                'verbose_name_plural': '友情链接',
                'verbose_name': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='Siteinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='网站标题')),
                ('icon', models.ImageField(upload_to='icon', verbose_name='网站图标')),
                ('url', models.URLField(max_length=120, verbose_name='网站url')),
                ('description', models.TextField(blank=True, verbose_name='网站简介')),
                ('privacy_policy', models.TextField(blank=True, verbose_name='隐私政策')),
                ('terms_of_service', models.TextField(blank=True, verbose_name='服务条款')),
            ],
            options={
                'verbose_name_plural': '网站信息',
                'verbose_name': '网站信息',
            },
        ),
    ]
