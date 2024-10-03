from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.db import transaction

from ..serializers import UserUpdateSerializer, UserSerializer
from apps.decorators.response_handler import response_handler


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
