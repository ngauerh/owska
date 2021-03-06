# Generated by Django 2.1.8 on 2019-05-24 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '板块',
                'verbose_name_plural': '板块',
            },
        ),
        migrations.CreateModel(
            name='Collected',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollectedBoard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Board')),
                ('starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('stars', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('comment_num', models.IntegerField(default=0)),
                ('path', models.CharField(max_length=250, unique=True, verbose_name='路径')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='forum.Board')),
                ('starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, max_length=100, to='forum.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '主题',
                'verbose_name_plural': '主题',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='forum.Topic'),
        ),
        migrations.AddField(
            model_name='comments',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Topic'),
        ),
        migrations.AddField(
            model_name='collected',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Topic'),
        ),
    ]
