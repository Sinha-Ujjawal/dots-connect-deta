from django.urls import path
from .views import UserSignUp, UserLogIn

urlpatterns = [
    path("signup", UserSignUp.as_view(), name="user_signup"),
    path("token", UserLogIn.as_view(), name="token_obtain_pair"),
]
