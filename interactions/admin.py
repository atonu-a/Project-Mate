from django.contrib import admin
from .models import JoinRequest, Follow, Like,Comment,CommentLike, Save

admin.site.register(JoinRequest)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Save)

# Register your models here.
