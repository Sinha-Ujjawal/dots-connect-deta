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
                data=[
                    {"roomId": "...32232xcxxcssss-aasxscsc-scssss...", "host": 1},
                    {"roomId": "...xss2xcxxcsssdsdsds-aasxscsc-scssss...", "host": 2},
                    {"roomId": "...sdsdxcxxcssdsaqw-aasxscsc-scssss...", "host": None},
                ]
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
