from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import get_user_model
User = get_user_model()

from blog.models import Blog, Tag
from blog.views import get_blog_by_id, get_tag_by_id


def get_user_by_id(id):
    try:
        user = User.objects.get(id=id)
        return user
    except User.DoesNotExist:
        return None


def save_blog(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot save a post unless you Login.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if blog:
        user.profile.save_blog(blog)
        context['blog'] = blog
    else:
        return HttpResponse(f'<div class="alert alert-info">Invalid blog.</div>')

    return render(request, 'blog/snippets/blog_options.html', context)


def unsave_blog(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot unsave a post unless you Login.</div>')

    context = {}
    blog_id = kwargs.get('blog_id')
    blog = get_blog_by_id(blog_id)

    if blog:
        user.profile.unsave_blog(blog)
        context['blog'] = blog
    else:
        return HttpResponse(f'<div class="alert alert-info">Invalid blog.</div>')

    return render(request, 'blog/snippets/blog_options.html', context)


def get_blogs(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        messages.info(request, 'You cannot retrive blogs unless you Login.')
        return redirect('home')

    saved = None
    account = None

    try:
        saved = kwargs.get('saved')
    except:
        saved = None

    try:
        account_id = kwargs.get('account_id')
    except:
        account_id = None

    if account_id:
        account = get_user_by_id(account_id)
    

    context = {}
    
    if saved:
        blog_objects = user.profile.saved_blogs.filter(status = '1')
    elif account:
        blog_objects = Blog.objects.filter(user=account).filter(status='1')
    else:
        blog_objects = Blog.objects.filter(user=user)

    paginator = Paginator(blog_objects, 5)
    page = request.GET.get('page')

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    
    context['blogs'] = blogs

    return render(request, 'accountProfile/display_blogs.html', context)


def get_followers_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        messages.info(request, 'You cannot see followers list unless you Login.')
        return redirect('home')

    context = {}
    followers = user.profile.followed_by.all()
    if len(followers) > 0:
        context['users'] = followers
    else:
        context['users'] = None

    return render(request, 'account/account_search.html', context)


def get_following_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        messages.info(request, 'You cannot get your following list unless you Login.')
        return redirect('home')

    context = {}
    following = user.profile.following.all()
    if len(following) > 0:
        context['users'] = following
    else:
        context['users'] = None

    return render(request, 'account/account_search.html', context)


def follow_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot follow someone unless you Login.</div>')

    context = {}
    account_id = kwargs.get('account_id')
    account = get_user_by_id(account_id)

    user.profile.follow(account)
    context['user'] = account

    return render(request, 'account/snippets/follow_chunk.html', context)


def unfollow_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot unfollow someone unless you Login.</div>')

    context = {}
    account_id = kwargs.get('account_id')
    account = get_user_by_id(account_id)

    user.profile.unfollow(account)
    context['user'] = account

    return render(request, 'account/snippets/follow_chunk.html', context)


def get_tags_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">Not available.</div>')

    context = {}
    tags = Tag.objects.all()
    context['tags'] = tags

    return render(request, 'accountProfile/snippets/tags.html', context)


def add_tags_to_profile(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot update your profile unless you Login.</div>')

    context = {}
    tag_id = kwargs.get('tag_id')
    tag = get_tag_by_id(tag_id)
    context['tag'] = tag

    user.profile.add_tag(tag)

    tags = Tag.objects.all()
    context['tags'] = tags

    return render(request, 'accountProfile/snippets/tags.html', context)


def remove_tags_from_profile(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f'<div class="alert alert-info">You cannot update your profile you Login.</div>')

    context = {}
    tag_id = kwargs.get('tag_id')
    tag = get_tag_by_id(tag_id)
    context['tag'] = tag

    user.profile.remove_tag(tag)

    tags = Tag.objects.all()
    context['tags'] = tags

    return render(request, 'accountProfile/snippets/tags.html', context)
