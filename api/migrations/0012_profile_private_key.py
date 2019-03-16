# Generated by Django 2.1.2 on 2019-03-15 08:25

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api", "0011_make_event_profile_optional")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="private_key",
            field=models.CharField(default=api.models.random_key, max_length=36),
        )
    ]
