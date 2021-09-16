from django.urls import path
from .views import UserMe, UserChangePassword

urlpatterns = [
    path("me", UserMe.as_view(), name="user_me"),
    path("changePassword", UserChangePassword.as_view(), name="user_change_password"),
]
