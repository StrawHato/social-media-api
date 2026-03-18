from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import routers

from user.views import (
    CreateUserView,
    UserViewSet
)


router = routers.SimpleRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("registration/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "user"
