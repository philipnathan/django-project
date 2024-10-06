from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from django.utils.decorators import method_decorator

from apps.decorators.response_handler import response_handler
from ..serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @method_decorator(response_handler)
    @method_decorator(transaction.atomic)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"email": user.email, "fullname": user.fullname, "role": user.role},
            status=status.HTTP_201_CREATED,
        )
