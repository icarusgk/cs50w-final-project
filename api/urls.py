from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView
)

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'stats', views.StatsViewSet)
router.register(r'modes', views.ModeViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('currentTask/', views.CurrentTaskView.as_view()),
  path('currentMode/', views.CurrentModeView.as_view()),
  path('tagInfo/<str:name>/', views.TagInfo.as_view()),
  
  # User Router
  path('register/', views.RegisterView.as_view()),
  path('me/', views.CurrentUserView.as_view()),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
