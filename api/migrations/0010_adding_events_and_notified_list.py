# Generated by Django 2.1.2 on 2019-03-11 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190202_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('task_done', 'Task done'), ('task_undone', 'Task undone'), ('list_completed', 'List completed'), ('task_added', 'Task added'), ('list_created', 'List created'), ('task_edited', 'Task edited'), ('list_edited', 'List edited')], max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('old_value', models.TextField(blank=True, null=True)),
                ('new_value', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='list',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='lists_to_notify',
            field=models.ManyToManyField(related_name='users_to_notify', to='api.List'),
        ),
        migrations.AddField(
            model_name='event',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.List'),
        ),
        migrations.AddField(
            model_name='event',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Profile'),
        ),
        migrations.AddField(
            model_name='event',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Task'),
        ),
    ]
