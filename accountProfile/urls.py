from django.urls import path

from accountProfile.views import (
    save_blog,
    unsave_blog,
    get_blogs,

    get_followers_view,
    get_following_view,
    follow_view,
    unfollow_view,

    get_tags_view,
    add_tags_to_profile,
    remove_tags_from_profile,
)

app_name = 'accountProfile'


urlpatterns = [
    path('save_blog/<blog_id>/', save_blog, name='save-blog'),
    path('unsave_blog/<blog_id>/', unsave_blog, name='unsave-blog'),
    path('get_blogs/', get_blogs, name='get-blogs'),
    path('get_blogs/<saved>/', get_blogs, name='get-saved-blogs'),
    path('get_blogs/user/<account_id>/', get_blogs, name='get-user-blogs'),

    path('get_followers/', get_followers_view, name='get-followers'),
    path('get_following/', get_following_view, name='get-following'),
    path('follow/<account_id>/', follow_view, name='follow'),
    path('unfollow/<account_id>/', unfollow_view, name='unfollow'),

    path('get_tags/', get_tags_view, name='get-tags'),
    path('add_tag_to_profile/<tag_id>/', add_tags_to_profile, name='add-tag-to-profile'),
    path('remove_tag_from_profile/<tag_id>/', remove_tags_from_profile, name='remove-tag-from-profile'),
]
