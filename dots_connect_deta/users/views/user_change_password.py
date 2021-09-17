from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.response import create_response, create_response_dict

from ..services import user_change_password

example_responses = {
    "204": openapi.Response(
        description="Password Changed Successfully",
        examples={
            "application/json": create_response_dict(status=status.HTTP_204_NO_CONTENT)
        },
    )
}


class InputSerializer(serializers.Serializer):
    oldPassword = serializers.CharField()
    newPassword = serializers.CharField()

    class Meta:
        ref_name = "UserChangePasswordInputSerializer"


class UserChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Change User's Password",
        request_body=InputSerializer,
        responses=example_responses,
    )
    def put(self, request):
        serializer = InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_data = serializer.validated_data

        user = request.user

        if user_change_password(
            user=user,
            old_password=request_data["oldPassword"],
            new_password=request_data["newPassword"],
        ):
            return create_response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("Old Password Incorrect!")
