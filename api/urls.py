from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

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
    path('me/', views.CurrentUserView.as_view()),

    # New JWT routes
    path('auth/register/', views.RegisterJWTView.as_view(), name='register'),
    path('auth/login/', views.LoginJWTView.as_view(), name='login'),
    path('auth/logout/', views.LogoutJWTView.as_view(), name='logout'),
]
