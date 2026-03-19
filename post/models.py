import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Hashtag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return f"{self.owner.username}: {self.content}"


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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts")
    comments = models.ManyToManyField(Comment, related_name="posts")

    def __str__(self):
        return self.content
