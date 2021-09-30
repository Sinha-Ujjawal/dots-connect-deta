from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.response import create_response, create_response_dict

from ..selectors import room_get_rooms, room_get_data

example_responses = {
    "200": openapi.Response(
        description="List of rooms",
        examples={
            "application/json": create_response_dict(
                data=[{"roomId": 4, "name": "xyz"}]
            )
        },
    )
}


class ListRooms(APIView):
    @swagger_auto_schema(
        operation_description="List all the rooms created by a user",
        responses=example_responses,
    )
    def get(self, request):
        user = request.user
        return create_response(
            data=[room_get_data(room=room) for room in room_get_rooms(user=user)]
        )
