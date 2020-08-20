from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import BlogPostForm

def index(request):
    """The home page for blogs. Show all posts."""
    posts = BlogPost.objects.order_by('date_added')
    context = {'posts': posts}
    return render(request, 'blogs/index.html', context)

def post(request, post_id):
    """Show a post."""
    post = get_object_or_404(BlogPost, id=post_id)
    context = {'post': post}
    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    """Add a new post"""
    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = BlogPostForm()
    else:
        # POST data submitted; process data.
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:index')
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing post."""
    post = BlogPost.objects.get(id=post_id)
    title = post.title
    text = post.text

    check_post_owner(request, post)
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = BlogPostForm(instance=post, data= request.POST, files= request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post.id)

    context = {'form': form, 'post': post}
    return render(request, 'blogs/edit_post.html', context)


def check_post_owner(request, post):
    """ Check if the topic belongs to the current user."""
    if post.owner != request.user:
        raise Http404