from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'streak']


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
  # user = serializers.ReadOnlyField(source='user.username')


  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'estimated', 
             'gone_through', 'minutes', 'done', 'tags', 'subtasks', 'project_tasks']
    depth = 1

class SubtaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subtask
    fields = ['id', 'title', 'description', 'done']


class ProjectSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source='user.username')      


  def get_fields(self):
    fields = super(ProjectSerializer, self).get_fields()
    fields['tasks'] = TaskSerializer(many=True)
    return fields


  class Meta:
    model = Project
    fields = ['id', 'name', 'tasks', 'user']
    depth = 2
    