from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from common.response import create_response, create_response_dict

from ..selectors import user_get_login_data

example_responses = {
    "200": openapi.Response(
        description="User's info",
        examples={
            "application/json": create_response_dict(
                data={"id": 1, "email": "admin@admin.com"}
            )
        },
    )
}


class UserMe(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get User's Info",
        responses=example_responses,
    )
    def get(self, request):
        return create_response(data=user_get_login_data(user=request.user))
