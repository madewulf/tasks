# Generated by Django 2.1.2 on 2018-11-06 05:53

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181102_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='list',
            name='key',
            field=models.CharField(default=api.models.random_key, max_length=36),
        ),
        migrations.AlterField(
            model_name='task',
            name='key',
            field=models.CharField(default=api.models.random_key, max_length=36),
        ),
    ]
