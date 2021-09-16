from rest_framework.exceptions import AuthenticationFailed, ValidationError

from rest_framework_simplejwt.authentication import JWTAuthentication, api_settings
from rest_framework_simplejwt.exceptions import TokenError


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                token_class = AuthToken.__name__
                message = f"{token_class}: {e.args[0]}"
                messages.append(message)

        raise AuthenticationFailed(detail=messages, code="token_not_valid")

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise ValidationError("Token contained no recognizable user identification")

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")

        return user
