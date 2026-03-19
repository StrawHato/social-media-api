from rest_framework import serializers

from post.models import (
    Hashtag,
    Comment,
    Post,
)


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content", "owner")

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "content", "owner", "picture", "hashtags")
        read_only_fields = ("id", "owner",)
