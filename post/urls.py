from django.urls import path, include

from rest_framework import routers

from post.views import (
    HashtagViewSet,
    PostViewSet,
    CommentViewSet
)


router = routers.DefaultRouter()
router.register("hashtags", HashtagViewSet)
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "post"
