# Generated by Django 2.1 on 2019-05-18 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='biography',
            field=models.TextField(null=True, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.CharField(max_length=50, null=True, verbose_name='所在公司'),
        ),
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.CharField(max_length=50, null=True, verbose_name='github'),
        ),
        migrations.AddField(
            model_name='user',
            name='instagram',
            field=models.CharField(max_length=50, null=True, verbose_name='instagram'),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin',
            field=models.CharField(max_length=50, null=True, verbose_name='linkedin'),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=50, null=True, verbose_name='所在地'),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram',
            field=models.CharField(max_length=50, null=True, verbose_name='telegram'),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.CharField(max_length=50, null=True, verbose_name='twitter'),
        ),
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(max_length=100, null=True, verbose_name='个人网站'),
        ),
        migrations.AddField(
            model_name='user',
            name='weibo',
            field=models.CharField(max_length=50, null=True, verbose_name='微博'),
        ),
    ]