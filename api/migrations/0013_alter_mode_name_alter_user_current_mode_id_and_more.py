# Generated by Django 4.1.1 on 2022-09-30 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_user_current_mode_id_alter_mode_short_break'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mode',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='current_mode_id',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='current_task_id',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
