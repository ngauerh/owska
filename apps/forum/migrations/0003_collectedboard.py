# Generated by Django 2.1.8 on 2019-05-23 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_collected'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectedBoard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Board')),
                ('starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
