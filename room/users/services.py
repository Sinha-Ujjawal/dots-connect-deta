from rest_framework.fields import ImageField
from .models import User

user_create = User.objects.create_user


def user_change_password(*, user: User, old_password: str, new_password: str) -> bool:
    if user.check_password(raw_password=old_password):
        if old_password != new_password:
            user.set_password(raw_password=new_password)
            user.save()
        return True
    else:
        return False
