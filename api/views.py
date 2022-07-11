from .serializers import *
from .models import Task
from django.http import Http404
from django.shortcuts import get_object_or_404
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
  
  def list(self, request):
    serializer = TagSerializer(self.queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    tag = get_object_or_404(self.queryset, pk=pk)
    serializer = TagTasksSerializer(tag)
    return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
