"""room URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, URLPattern
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="room API",
        default_version="v1.0.0",
        description="room is a ...",  # TODO
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(url="https://github.com/Sinha-Ujjawal"),
        # license=openapi.License(name="MIT License"), TODO
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def path_with_base(base_url: str):
    """Returns a function that adds a given prefix to all the paths generated from
    returned function
    """

    def _inner(route: str, *args, **kwargs) -> URLPattern:
        return path(f"{base_url}/{route}", *args, **kwargs)

    return _inner


base_path = path_with_base("room")


urlpatterns = [
    base_path(
        "playground/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    base_path(
        "docs/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    base_path("admin/", admin.site.urls),
    base_path("auth/", include("room.authentication.urls")),
    base_path("users/", include("room.users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
