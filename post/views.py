from django.db.models import Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from post.models import Hashtag, Post, Like, Comment
from post.permissions import IsOwnerOrReadOnly
from post.serializers import (
    HashtagSerializer,
    PostSerializer,
    PostListDetailSerializer,
    CommentSerializer, CommentListDetailSerializer
)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = (IsAuthenticated,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.select_related("owner")
        .prefetch_related("hashtags")
        .annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        )
    )
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        followings = self.request.user.following.all()
        user_ids = [f.following.id for f in followings] + [self.request.user.id]
        queryset = self.queryset.filter(owner__id__in=user_ids)

        hashtags = self.request.query_params.get("hashtags")
        author = self.request.query_params.get("author")
        content = self.request.query_params.get("content")

        if author:
            queryset = queryset.filter(
                owner__username__icontains=author,
            )
        if content:
            queryset = queryset.filter(
                content__icontains=content,
            )
        if hashtags:
            queryset = queryset.filter(
                hashtags__id__in=[int(hashtag) for hashtag in hashtags.split(",")],
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PostListDetailSerializer
        if self.action in ("comment", "comments"):
            return CommentSerializer
        return PostSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        target_post = self.get_object()

        like, created = Like.objects.get_or_create(
            post=target_post,
            user=request.user,
        )

        if not created:
            return Response(
                {"Error": "You are already liked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"Success": "You liked this post"},
            status=status.HTTP_200_OK
        )

    @like.mapping.delete
    def unlike(self, request, pk=None):
        target_post = self.get_object()
        like = Like.objects.filter(
                post=target_post,
                user=request.user
        )

        if like.exists():
            like.delete()

            return Response(
                {"Status": "You unliked this post"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"Error": "Your like doesn't exist"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        target_post = self.get_object()
        comments = target_post.comments.all()
        serializer = self.get_serializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user, post=self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtags",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by hashtags (ex. ?hashtags=1,2)",
            ),
            OpenApiParameter(
                name="author",
                type=OpenApiTypes.STR,
                description="Filter by author (ex. ?author=username)",
            ),
            OpenApiParameter(
                name="content",
                type=OpenApiTypes.STR,
                description="Filter by content (ex. ?content=part of content)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Returns a filtered list of posts."""
        return super(PostViewSet, self).list(request, *args, **kwargs)


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.select_related(
        "owner", "post"
    )
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CommentListDetailSerializer
        return CommentSerializer
