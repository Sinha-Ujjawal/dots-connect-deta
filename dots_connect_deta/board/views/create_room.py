from rest_framework import serializers
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.response import create_response, create_response_dict

from ..services import room_create_room
from ..selectors import room_get_data

example_responses = {
    "200": openapi.Response(
        description="Room Created Successfully",
        examples={
            "application/json": create_response_dict(data={"roomId": 4, "name": "xyz"})
        },
    )
}


class CreateRoomSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        ref_name = "CreateRoomSerializer"


class CreateRoom(APIView):
    @swagger_auto_schema(
        operation_description="Create a Room with the given name",
        request_body=CreateRoomSerializer,
        responses=example_responses,
    )
    def put(self, request):
        serializer = CreateRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_data = serializer.validated_data

        user = request.user

        room = room_create_room(name=request_data["name"], user=user)

        return create_response(data=room_get_data(room=room))
