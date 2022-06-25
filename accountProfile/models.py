from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from django.contrib.auth import get_user_model
User = get_user_model()

from blog.models import Blog, Tag


class Profile(models.Model):
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.CharField(
        verbose_name=_('Bio'),
        blank=True,
        null=True,
        max_length=256,
    )
    following = models.ManyToManyField(
        User,
        related_name='following',
        blank=True,
    )
    followed_by = models.ManyToManyField(
        User,
        related_name='followed_by',
        blank=True,
    )
    saved_blogs = models.ManyToManyField(
        Blog,
        related_name='saved_blogs',
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name=_('account_tags')
    )

    def __Str__(self):
        return self.user.username

    def follow(self, user):
        if not user in self.following.all():
            self.following.add(user)

        if not self.user in user.profile.followed_by.all():
            user.profile.followed_by.add(self.user)

    def unfollow(self, user):
        if user in self.following.all():
            self.following.remove(user)

        if self.user in user.profile.followed_by.all():
            user.profile.followed_by.remove(self.user)

    def save_blog(self, blog):
        if not blog in self.saved_blogs.all():
            self.saved_blogs.add(blog)

    def unsave_blog(self, blog):
        if blog in self.saved_blogs.all():
            self.saved_blogs.remove(blog)

    def add_tag(self, tag):
        if not tag in self.tags.all():
            self.tags.add(tag)

    def remove_tag(self, tag):
        if tag in self.tags.all():
            self.tags.remove(tag)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
