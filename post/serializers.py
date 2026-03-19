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


class PostListDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    hashtags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    likes = serializers.IntegerField(
        source="likes_count",
        read_only=True
    )
    comments = serializers.IntegerField(
        source="comments_count",
        read_only=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "owner",
            "picture",
            "hashtags",
            "likes",
            "comments"
        )
