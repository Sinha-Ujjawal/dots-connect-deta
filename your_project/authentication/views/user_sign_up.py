from django.contrib.auth import login

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from common.response import create_response, create_response_dict

from room.users.selectors import user_get_login_data, user_get_by_email
from room.users.services import user_create

from ..services import user_create_access_token


example_responses = {
    "201": openapi.Response(
        description="Successful creation of User",
        examples={
            "application/json": create_response_dict(
                data={
                    "id": 1,
                    "email": "xyz@abc.com",
                    "access": "exxddnjsjkdkdcdkdkcdkcdncdkndkk...",
                },
                status=status.HTTP_201_CREATED,
            )
        },
    ),
    "400": openapi.Response(
        description="User already exising!",
        examples={
            "application/json": {
                "errors": [{"message": "User already existing!", "code": "invalid"}],
                "data": None,
                "statusCode": 400,
            }
        },
    ),
}


class InputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        ref_name = "UserSignUpInputSerializer"


class UserSignUp(APIView):
    @swagger_auto_schema(
        security=[],
        request_body=InputSerializer,
        responses=example_responses,
    )
    def post(self, request):
        serializer = InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_data = serializer.validated_data

        user = user_get_by_email(email=request_data["email"])

        if user is None:
            user = user_create(
                email=request_data["email"], password=request_data["password"]
            )
            login(request=request, user=user)
            return create_response(
                data={
                    **user_get_login_data(user=user),
                    **user_create_access_token(user=user),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            raise ValidationError(detail="User already existing!")
