from typing import Any
from rest_framework.response import Response
from rest_framework import status


def create_response_dict(*, data: Any = None, status=status.HTTP_200_OK):
    return {"data": data, "errors": [], "statusCode": status}


def create_response(*, data: Any = None, status=status.HTTP_200_OK) -> Response:
    return Response(create_response_dict(data=data, status=status))
