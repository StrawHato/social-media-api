from django.db.models import Count
from rest_framework import viewsets

from post.models import Hashtag, Post
from post.serializers import HashtagSerializer, PostSerializer, PostListDetailSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
