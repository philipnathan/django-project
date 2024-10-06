from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound


def response_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotFound as e:
            return Response(
                {"error": e.detail},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
