from rest_framework_simplejwt.tokens import RefreshToken
from dots_connect_deta.users.models import User


def user_create_access_token(*, user: User):
    return {"access": str(RefreshToken.for_user(user=user).access_token)}
