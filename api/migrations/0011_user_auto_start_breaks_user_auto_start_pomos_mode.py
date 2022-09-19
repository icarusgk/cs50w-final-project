# Generated by Django 4.1.1 on 2022-09-19 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_done_stats_chores_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auto_start_breaks',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='auto_start_pomos',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('pomo', models.IntegerField(default=25)),
                ('short_break', models.IntegerField(default=25)),
                ('long_break', models.IntegerField(default=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
