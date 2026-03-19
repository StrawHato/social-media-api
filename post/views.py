from django.db.models import Count
from rest_framework import viewsets

from post.models import Hashtag, Post
from post.serializers import HashtagSerializer, PostSerializer, PostListDetailSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.select_related("owner")
        .prefetch_related("hashtags")
        .annotate(
            likes_count=Count("likes"),
            comments_count=Count("comments"),
        )
    )
    serializer_class = PostSerializer

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
                owner__username=author,
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
        return PostSerializer
