from django.urls import path

from blog.views import (
    blog_create_view, 
    blog_detail_view, 
    blog_edit_view, 
    blog_delete_view,
    blog_update_view,

    post_add_view,
    post_update_view,
    post_delete_view,
    
    blog_like_view,
    blog_dislike_view,
    comment_view,
    reply_view,
    get_blog_elements_view,

    get_tags_view,
    add_tags_to_blog,
    remove_tags_from_blog,
    publish_blog_view,
)

app_name = 'blog'

urlpatterns = [
    path('blog_create', blog_create_view, name='blog-create'),
    path('blog_detail/<blog_id>/', blog_detail_view, name='blog-detail'),
    path('blog_edit/<blog_id>/', blog_edit_view, name='blog-edit'),
    path('blog-delete/<blog_id>/', blog_delete_view, name='blog-delete'),
    path('blog_update/<blog_id>/', blog_update_view, name='blog-update'),

    path('post_add/<blog_id>/', post_add_view, name='post-add'),
    path('post_update/<post_id>/', post_update_view, name='post-update'),
    path('post_delete/<post_id>/', post_delete_view, name='post-delete'),

    path('blog_like/<blog_id>/', blog_like_view, name='like-blog'),
    path('blog_dislike/<blog_id>/', blog_dislike_view, name='dislike-blog'),
    path('blog_comment/<blog_id>/', comment_view, name='comment-blog'),
    path('comment_reply/<comment_id>/', reply_view, name='reply-comment'),
    path('get_blog_elements/<blog_id>/', get_blog_elements_view, name='get-blog-elements'),
    path('get_blog_elements/<blog_id>/<partial>/',get_blog_elements_view, name='get-blog-elements'),

    path('get_tags/<blog_id>/', get_tags_view, name='get-tags'),
    path('add_tag_to_blog/<blog_id>/<tag_id>/', add_tags_to_blog, name='add-tag-to-blog'),
    path('remove_tag_from-blog/<blog_id>/<tag_id>/', remove_tags_from_blog, name='remove-tag-from-blog'),
    path('publish_blog/<blog_id>/', publish_blog_view, name='publish-blog'),
]
