from django.contrib import admin

from blog.models import Tag, Blog, Post, Comment, Reply


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_diaplay = ('name', )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('user' ,'heading', 'status', 'date_published', 'date_created')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'content', 'date_created')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'date_time')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'date_time')

