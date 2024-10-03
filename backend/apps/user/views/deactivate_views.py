from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from django.utils.decorators import method_decorator

from ..serializers import UserSerializer, UserDeactivateSerializer

from apps.decorators.response_handler import response_handler


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
