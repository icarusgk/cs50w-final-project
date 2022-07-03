from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email', 'streak']


class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = ['id', 'user', 'title', 'description', 'subtasks']
    