from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'auto_start_pomos',
            'auto_start_breaks',
            'current_task_id']


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ['id', 'day', 'chores_done']


class ModesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode
        exclude = ['user']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'estimated',
            'gone_through',
            'done',
            'tags',
            'subtasks',
            'project_tasks']
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super(ProjectSerializer, self).get_fields()
        fields['tasks'] = TaskSerializer(many=True)
        return fields

    class Meta:
        model = Project
        fields = ['id', 'name', 'tasks']
        depth = 2
