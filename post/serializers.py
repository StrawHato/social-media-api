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
