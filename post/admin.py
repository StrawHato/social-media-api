from django.contrib import admin

from post.models import Post, Hashtag, Comment, Like


admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Comment)
admin.site.register(Like)
