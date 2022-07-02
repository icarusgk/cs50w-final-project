from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import *
from .models import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  