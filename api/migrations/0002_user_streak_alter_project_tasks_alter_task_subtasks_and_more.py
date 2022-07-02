# Generated by Django 4.0.1 on 2022-07-02 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='tasks',
            field=models.ManyToManyField(blank=True, to='api.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.ManyToManyField(blank=True, to='api.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, to='api.Tag'),
        ),
    ]
