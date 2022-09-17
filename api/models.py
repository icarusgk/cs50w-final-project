from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Tag(models.Model):
  name = models.CharField(max_length=20, unique=True)

  def __str__(self):
    return f'#{self.name}'


class User(AbstractUser):
  current_task_id = models.IntegerField(default=0)

class Task(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tasks')
  title = models.CharField(max_length=50)
  description = models.TextField(max_length=255, blank=True)
  estimated = models.IntegerField(default=0)
  gone_through = models.IntegerField(default=0)
  minutes = models.IntegerField(default=0)
  tags = models.ManyToManyField('Tag', blank=True, related_name='tags')
  done = models.BooleanField(default=False)
  in_project = models.BooleanField(default=False)

  def __str__(self):
    return f'Task: {self.title}'


class Subtask(models.Model):
  task = models.ForeignKey('Task', related_name='subtasks', on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  description = models.TextField(max_length=255, blank=True)
  done = models.BooleanField(default=False)

  def __str__(self):
    return f'Subtask: {self.title} - {self.done}'


class Project(models.Model):
  name = models.CharField(max_length=30)
  user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='projects')
  tasks = models.ManyToManyField('Task', blank=True, related_name='project_tasks')

  def __str__(self):
    return f'Project: {self.name}'


class Stats(models.Model):
  day = models.DateField(default=timezone.now, null=False)
  done = models.IntegerField(default=0)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stats')

  def __str__(self):
    return f'{self.user} has done {self.done} on {self.day}'