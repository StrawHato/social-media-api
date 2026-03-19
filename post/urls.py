from django.urls import path, include

from rest_framework import routers

from post.views import HashtagViewSet


router = routers.DefaultRouter()
router.register("hashtags", HashtagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "post"
