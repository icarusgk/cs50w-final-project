from .serializers import TaskSerializer
from .models import Task
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class TaskList(APIView):
  """
  List all tasks or one, or create a new task
  """
  def get(self, request, format=None, id=None):
    if id:
      task = Task.objects.get(id=id)
      return Response(TaskSerializer(task).data)

    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)