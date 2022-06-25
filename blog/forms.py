from django import forms

from blog.models import Blog, Post, Comment, Reply


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['heading', 'description']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
