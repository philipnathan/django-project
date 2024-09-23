from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("create/", views.UserCreateView.as_view(), name="user_create"),
    path("me/", views.UserRetrieveView.as_view(), name="user_retrieve"),
    path("me/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("login/", TokenObtainPairView.as_view(), name="user_login"),
    path("refreshtoken/", TokenRefreshView.as_view(), name="user_refreshtoken"),
]
