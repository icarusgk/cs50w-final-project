from django.urls import path
from api import views

urlpatterns = [
  path('tasks/', views.TaskList.as_view()),
  path('tasks/<int:id>', views.TaskList.as_view())
]
