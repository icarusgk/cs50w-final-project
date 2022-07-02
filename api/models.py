from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser, models.Model):
  streak = models.IntegerField(default=0)


class Task(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  description = models.TextField(max_length=255)
  estimated = models.IntegerField(default=0)
  gone_through = models.IntegerField(default=0)
  minutes = models.IntegerField(default=0)
  subtasks = models.ManyToManyField('Task', blank=True)
  tags = models.ManyToManyField('Tag', blank=True)

  def __str__(self):
    return f'Task: {self.title}'


class Tag(models.Model):
  name = models.CharField(max_length=20, unique=True)

  def __str__(self):
    return f'#{self.name}'


class Project(models.Model):
  name = models.CharField(max_length=30)
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  tasks = models.ManyToManyField('Task', blank=True)

  def __str__(self):
    return f'Project: {self.name}'