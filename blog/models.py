from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from django.contrib.auth import get_user_model
User = get_user_model()


class Tag(models.Model):
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_('Tag Name'),
        max_length=64,
        unique=True
    )

    def __str__(self):
        return self.name


class Blog(models.Model):
    BLOG_STATUS = (
        ('0', 'draft'),
        ('1', 'published')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name=_('author'),
    )
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    heading = models.CharField(
        verbose_name=_('Title'),
        max_length=256
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True, 
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name=_('tags'),
        blank=True,
    )
    status = models.CharField(
        verbose_name=_('Blog Status'),
        max_length=16,
        choices=BLOG_STATUS,
        default='0',
    )
    date_published = models.DateTimeField(
        verbose_name=_('Published Date'),
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        verbose_name=_('Last Updated'),
        auto_now=True,
    )

    likes = models.ManyToManyField(
        User,
        related_name=_('likes'),
        blank=True,
    )
    dislikes = models.ManyToManyField(
        User,
        related_name=_('dislikes'),
        blank=True,
    )

    def __str__(self):
        return f'{self.heading}'

    @property
    def is_published(self):
        return self.status == '1'

    @property
    def get_posts(self):
        return self.posts.all()

    @property
    def get_likes(self):
        return self.likes.all()

    @property
    def get_dislikes(self):
        return self.dislikes.all()

    def like(self, user):
        if user in self.dislikes.all():
            self.dislikes.remove(user)

        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def dislike(self, user):
        if user in self.likes.all():
            self.likes.remove(user)

        if user in self.dislikes.all():
            self.dislikes.remove(user)
        else:
            self.dislikes.add(user)

    def add_tag(self, tag):
        if not tag in self.tags.all():
            self.tags.add(tag)

    def remove_tag(self, tag):
        if tag in self.tags.all():
            self.tags.remove(tag)

    def publish(self):
        self.status = '1'
        self.save()


    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ['-date_updated']


def get_post_image(post, filename):
    return f'post_images/{post.blog.user.id}/{filename}'


class Post(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name=_('posts')
    )
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    heading = models.CharField(
        verbose_name=_('Heading'),
        max_length=256,
        null=True,
        blank=True,
    )
    content = models.TextField(
        verbose_name=_('Content'),
    )
    image = models.ImageField(
        verbose_name=_('Image'),
        null=True,
        blank=True,
        upload_to=get_post_image,
    )
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.blog.title}-{self.content}'

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['date_created']


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name=_('comments')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    date_time = models.DateTimeField(
        verbose_name=_('Comment Date'),
        auto_now_add=True,
    )
    body = models.CharField(
        verbose_name=_('Body'),
        max_length=512,
    )

    def __self__(self):
        return f'{self.user} {self.body}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-date_time']


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name=_('replies')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    date_time = models.DateTimeField(
        verbose_name=_('Reply Date'),
        auto_now_add=True,
    )
    body = models.CharField(
        verbose_name=_('Body'),
        max_length=512,
    )

    def __self__(self):
        return f'{self.user} {self.body}'

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        ordering = ['date_time']
