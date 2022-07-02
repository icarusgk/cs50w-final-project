from .models import *
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email', 'streak']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Task
    fields = ['user', 'title', 'description', 'subtasks']
    