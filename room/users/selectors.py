from typing import Optional
from .models import User


def user_get_login_data(*, user: User):
    return {
        "id": user.id,
        "email": user.email,
    }


def user_get_by_email(*, email: str) -> Optional[User]:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def user_get_by_uid(*, userid: str) -> Optional[User]:
    try:
        return User.objects.get(id=userid)
    except User.DoesNotExist:
        return None
