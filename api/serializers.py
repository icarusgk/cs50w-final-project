from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email', 'streak']


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
  tags = TagSerializer(many=True)
  class Meta:
    model = Task
    exclude = ['user']
    depth = 1

  def get_fields(self):
    fields = super(TaskSerializer, self).get_fields()
    fields['subtasks'] = TaskSerializer(many=True)
    return fields

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    exclude = ['user']
    depth = 1
    