from .serializers import *
from .models import Task
from django.http import Http404
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


# This viewsets automatically provide `list`, `create`, `retrieve`,
# `update` and `destroy` actions.

# Create your views here.
# TODO: Convert to ListApiView for querying
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
