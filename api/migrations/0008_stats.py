# Generated by Django 4.1.1 on 2022-09-17 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_task_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(default=django.utils.timezone.now)),
                ('done', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
