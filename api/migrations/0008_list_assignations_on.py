# Generated by Django 2.1.2 on 2019-01-12 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_list_sort'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='assignations_on',
            field=models.BooleanField(default=True),
        ),
    ]
