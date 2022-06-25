from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages

import datetime

from blog.models import Blog, Post, Comment ,Reply, Tag
from blog.forms import BlogForm, PostForm


def get_blog_by_id(id):
    try:
        blog = Blog.objects.get(id=id)
        return blog
    except Blog.DoesNotExist:
        return None


def get_post_by_id(id):
    try:
        post = Post.objects.get(id=id)
        return post
    except Post.DoesNotExist:
        return None


def get_comment_by_id(id):
    try:
        comment = Comment.objects.get(id=id)
        return comment
    except Comment.DoesNotExist:
        return None


def get_tag_by_id(id):
    try:
        tag = Tag.objects.get(id=id)
        return tag
    except Tag.DoesNotExist:
        return None


def blog_create_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'You must login to create or update your blogs.')
        return redirect('account:login')

    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = user
            blog.save()
            form.save_m2m()

            messages.success(request, f'Blog created successfully.')
            return redirect('blog:blog-detail', blog_id = blog.id)
        else:
            context['form'] = form

    if request.method == 'GET':
        form = BlogForm()
        context['form'] = form
    return render(request, 'blog/blog_add.html', context)


def blog_detail_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if not user.is_authenticated:
        messages.warning(
            request, 'You must login to view blogs or posts.')
        return redirect('account:login')

    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if not blog:
        messages.warning(request, 'Sorry!, blog not available.')
        return redirect('home')

    context['blog'] = blog
    return render(request, 'blog/blog_detail.html', context)


def blog_edit_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if not user.is_authenticated:
        messages.warning(
            request, 'You must login to create or update your blogs or posts.')
        return redirect('account:login')

    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if not blog:
        messages.warning(request, 'Sorry!, blog not available.')
        return redirect('home')

    context['blog'] = blog

    if not blog.user == request.user:
        messages.warning(request, 'You cannot edit other persons blog.')
        return redirect('home')

    return render(request, 'blog/blog_edit.html', context)


def blog_update_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You must login to create or update your blogs or posts.</div>')

    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if not blog:
        return HttpResponse(f'<div class="alert alert-info">Sorry!, blog not available.</div>')

    if not blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot update other persons blog.</div>')

    if request.method == "GET":
        form = BlogForm(instance=blog)
        context['blog'] = blog
        context['form'] = form
        return render(request, 'blog/snippets/blog_form.html', context)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            context['blog'] = blog
            return render(request, 'blog/snippets/blog.html', context)
        else:
            context['form'] = form
            context['blog'] = blog
            return render(request, 'blog/snippets/blog_form.html', context)


def blog_delete_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You must login to delete your blogs or posts.</div>')

    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if not blog:
        return HttpResponse(f'<div class="alert alert-info">Sorry!, blog not available.</div>')

    if not blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot delete other persons blog.</div>')

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted successfully.')
        return redirect('home')

    if request.method == 'GET':
        context['blog'] = blog

    return render(request, 'blog/blog_delete.html', context)


def post_add_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You must login to add posts.</div>')

    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if not blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot update other persons blog.</div>')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.blog = blog
            post.save()
            context['post'] = post
            return render(request, 'blog/snippets/post.html', context)
        else:
            context['form'] = form
            context['post'] = {'id': 'id-temp'} 
            return render(request, 'blog/snippets/post_add_form.html', context)

    if request.method == 'GET':
        form = PostForm()
        context['form'] = form
        context['blog'] = blog
        context['post'] = {'id': 'id-temp'}
    return render(request, 'blog/snippets/post_add_form.html', context)


def post_update_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You must login to create or update your blogs or posts.</div>')

    post_id = kwargs.get('post_id')
    post = get_post_by_id(post_id)

    if not post:
        return HttpResponse(f'<div class="alert alert-info">Sorry!, post not available.</div>')

    if not post.blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot update other persons post.</div>')

    if request.method == "GET":
        form = PostForm(instance=post)
        context['post'] = post
        context['form'] = form
        return render(request, 'blog/snippets/post_form.html', context)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            context['post'] = post
            return render(request, 'blog/snippets/post.html', context)
        else:
            context['post'] = post
            context['form'] = form
            return render(request, 'blog/snippets/post_form.html', context)


def post_delete_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You must login to delete your blogs or posts.</div>')

    post_id = kwargs.get('post_id')
    post = get_post_by_id(post_id)

    if not post:
        return HttpResponse(f'<div class="alert alert-info">Sorry!, post not available.</div>')

    if not post.blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot delete other persons post.</div>')

    post.delete()
    return HttpResponse()


def blog_like_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot like a post unless you Login.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if blog:
        blog.like(user)

        context['blog'] = blog
    else:
        return HttpResponse(f'<div class="alert alert-info">Invalid blog.</div>')

    return render(request, 'blog/snippets/blog_options.html', context)


def blog_dislike_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot dislike a post unless you Login.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if blog:
        blog.dislike(user)

        context['blog'] = blog
    else:
        return HttpResponse(f'<div class="alert alert-info">Invalid blog.</div>')

    return render(request, 'blog/snippets/blog_options.html', context)


def comment_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You must login to comment on post.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if request.method == 'POST':
        body = request.POST.get('comment-input', '')
        if blog:
            comment = Comment.objects.create(blog=blog, user=request.user, body=body)
            context['comment'] = comment
        else:
            return HttpResponse(f'<div class="alert alert-info">Invalid blog.</div>')

    return render(request, 'blog/snippets/comment.html', context)


def reply_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You must login to reply on comment.</div>')

    context = {}
    comment_id = kwargs.get('comment_id')
    comment = get_comment_by_id(comment_id)

    if request.method == 'POST':
        body = request.POST.get('reply-input', '')
        if comment:
            reply = Reply.objects.create(comment=comment, user=request.user, body=body)
            context['reply'] = reply
        else:
            return HttpResponse(f'<div class="alert alert-info">Invalid blog.</div>')

    return render(request, 'blog/snippets/reply.html', context)


def get_blog_elements_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot like a post unless you Login.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if blog:
        context['blog'] = blog
    else:
        return HttpResponse(f'<div class="alert alert-info">Invalid blog.</div>')

    try:
        partial = kwargs.get('partial')
    except:
        partial = None

    if partial:
        return render(request, 'snippets/blog_elements.html', context)

    return render(request, 'blog/snippets/blog_elements.html', context)


def get_tags_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">Not available.</div>') 

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)
    context['blog'] = blog

    tags = Tag.objects.all()
    context['tags'] = tags

    return render(request, 'blog/snippets/tags.html', context)


def add_tags_to_blog(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot update a blog unless you Login.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)
    context['blog'] = blog

    tag_id = kwargs.get('tag_id')
    tag = get_tag_by_id(tag_id)
    context['tag'] = tag

    if not blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot update other persons blog.</div>')

    blog.add_tag(tag)

    tags = Tag.objects.all()
    context['tags'] = tags

    return render(request, 'blog/snippets/tags.html', context)


def remove_tags_from_blog(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot update a blog unless you Login.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)
    context['blog'] = blog

    tag_id = kwargs.get('tag_id')
    tag = get_tag_by_id(tag_id)
    context['tag'] = tag

    if not blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot update other persons blog.</div>')

    blog.remove_tag(tag)

    tags = Tag.objects.all()
    context['tags'] = tags

    return render(request, 'blog/snippets/tags.html', context)


def publish_blog_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot publish a blog unless you Login.</div>')

    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if not blog.user == request.user:
        return HttpResponse(f'<div class="alert alert-info">You cannot publish other persons blog.</div>')

    blog.publish()
    blog.date_published = datetime.datetime.now()
    blog.save()

    return HttpResponse()
