from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  pass


class Task(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  description = models.TextField(max_length=255)
  estimated = models.IntegerField()
  gone_through = models.IntegerField()
  minutes = models.IntegerField()
  subtasks = models.ManyToManyField('Task', blank=True)
  tags = models.ManyToManyField('Tag', blank=True)


class Tag(models.Model):
  name = models.CharField(max_length=20)


class Project(models.Model):
  name = models.CharField(max_length=30)
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  tasks = models.ManyToManyField('Task', blank=True)
