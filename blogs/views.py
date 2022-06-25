from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 

from blog.models import Blog

def home(request, *args, **kwargs):
    context = {}

    blog_objects = Blog.objects.filter(status='1')

    paginator = Paginator(blog_objects, 5)
    page = request.GET.get('page')

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context ['blogs'] = blogs
    return render(request, 'home.html', context)

def page_not_found_view(request, *args, **kwargs):
    return render(request, '404.html', status=404)
