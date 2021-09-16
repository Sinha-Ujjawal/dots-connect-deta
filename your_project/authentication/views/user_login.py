from django.contrib.auth import authenticate, login

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from common.response import create_response, create_response_dict

from ..services import user_create_access_token

example_responses = {
    "200": openapi.Response(
        description="Successful login of User",
        examples={
            "application/json": create_response_dict(
                data={"access": "exxddnjsjkdkdcdkdkcdkcdncdkndkk..."}
            )
        },
    ),
    "401": openapi.Response(
        description="User Unauthrorized",
        examples={
            "errors": [
                {"message": "Invalid Credentials!", "code": "authentication_failed"}
            ],
            "data": None,
            "statusCode": 401,
        },
    ),
}


class InputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        ref_name = "UserLogInInputSerializer"


class UserLogIn(APIView):
    @swagger_auto_schema(
        security=[],
        request_body=InputSerializer,
        responses=example_responses,
    )
    def post(self, request):
        serializer = InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_data = serializer.validated_data

        user = authenticate(request=request, **request_data)

        if user is None:
            raise AuthenticationFailed(detail="Invalid Credentials!")
        else:
            login(request=request, user=user)
            return create_response(data=user_create_access_token(user=user))
