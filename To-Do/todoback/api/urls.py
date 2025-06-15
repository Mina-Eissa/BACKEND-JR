from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskCRUD, TagCRUD, SignUpView,SignInView,PersonInfoView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

taskrouter = DefaultRouter()
taskrouter.register(r'tasks', TaskCRUD, basename='task')
tagrouter = DefaultRouter()
tagrouter.register(r'tags', TagCRUD, basename='tag')
urlpatterns = [
    path('', include(taskrouter.urls)),
    path('', include(tagrouter.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/<str:identifier>', SignInView.as_view(), name='signin'),
    path('personinfo/<str:identifier>',PersonInfoView.as_view(),name='personinfo')
]
