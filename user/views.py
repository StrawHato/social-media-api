from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import (
    generics,
    viewsets,
    status,
    permissions
)
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import Follow
from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserShortSerializer,
    UserProfileSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


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

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        target_user = self.get_object()

        if request.user == target_user:
            return Response(
                {"error": "You can't follow yourself!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            return Response(
                {"error": "Already following"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"status": f"Now you're following {target_user.username}"},
            status=status.HTTP_200_OK
        )

    @follow.mapping.delete
    def unfollow(self, request, pk=None):
        target_user = self.get_object()

        if Follow.objects.filter(
                follower=request.user,
                following=target_user
        ).exists():
            Follow.objects.filter(
                follower=request.user,
                following=target_user
            ).delete()

            return Response(
                {"status": "Unfollowed"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "You are not following this user!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["get"])
    def following(self, request, pk=None):
        target_user = self.get_object()
        following = target_user.following.all()

        serializer = UserShortSerializer(
            [f.following for f in following],
            many=True
        )

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        target_user = self.get_object()
        followers = target_user.followers.all()

        serializer = UserShortSerializer(
            [f.follower for f in followers],
            many=True
        )

        return Response(status=status.HTTP_200_OK, data=serializer.data)
