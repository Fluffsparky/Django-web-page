# Generated by Django 4.0.5 on 2023-03-05 19:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_rename_user_comments_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 5, 21, 50, 59, 865022)),
        ),
        migrations.RemoveField(
            model_name='comments',
            name='username',
        ),
        migrations.AddField(
            model_name='comments',
            name='username',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
