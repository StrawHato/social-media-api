from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import generics, viewsets

from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (get_user_model().objects.
        prefetch_related("followers__follower").
        annotate(
        followers_count=Count("followers"),
        following_count=Count("following"),
        )
    )
    serializer_class = UserListSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserListSerializer
