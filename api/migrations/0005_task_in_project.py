# Generated by Django 4.0.1 on 2022-08-20 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_task_subtasks_task_done_alter_project_tasks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='in_project',
            field=models.BooleanField(default=False),
        ),
    ]
