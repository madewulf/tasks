# Generated by Django 2.1.2 on 2018-11-06 17:34

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181106_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='key',
            field=models.CharField(default=api.models.random_key, max_length=36),
        ),
    ]
