# Generated by Django 2.1.2 on 2018-10-29 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='question_text',
        ),
    ]
