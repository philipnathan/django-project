from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from django.utils.decorators import method_decorator

from .serializers import UserSerializer, UserUpdateSerializer, UserDeactivateSerializer

from apps.decorators.response_handler import response_handler


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @method_decorator(response_handler)
    @method_decorator(transaction.atomic)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"email": user.email, "role": user.role}, status=status.HTTP_201_CREATED
        )


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @method_decorator(response_handler)
    @method_decorator(transaction.atomic)
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=self.request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {"message": "User updated successfully", "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class UserDeactivateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDeactivateSerializer

    def get_object(self):
        return self.request.user

    @method_decorator(response_handler)
    @method_decorator(transaction.atomic)
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data={"is_active": False}, partial=True)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "User deactivated successfully",
                "user": UserSerializer(user).data,
            },
        )
