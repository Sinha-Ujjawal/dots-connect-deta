from rest_framework.renderers import JSONRenderer
from rest_framework import status


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        assert data.keys() == {"data", "errors", "statusCode"}
        return super().render(
            data=data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )
