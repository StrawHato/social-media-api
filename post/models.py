import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Hashtag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def upload_post_picture(instance, filename):
    """Upload a post picture."""
    ext = filename.split(".")[-1]
    filename = f"{slugify(instance.owner.username)}-{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/posts/", filename)


class Post(models.Model):
    content = models.TextField()
    picture = models.ImageField(upload_to=upload_post_picture, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    hashtags = models.ManyToManyField(Hashtag, related_name="posts")

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_like_post"
            )
        ]


class Comment(models.Model):
    content = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username}: {self.content}"
