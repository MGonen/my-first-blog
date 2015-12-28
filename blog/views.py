from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
import operator
from itertools import chain

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=pk).order_by('created_date')

    already_published = True
    if not post.published_date or post.published_date > timezone.now():
        already_published = False

    return render(request, 'blog/post_detail.html', {'post':post, 'already_published':already_published, 'comments':comments })


def post_new(request):
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('post_list')

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if "publish" in request.POST:
                return redirect('post_publish', pk=post.pk)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":

        if "cancel" in request.POST:
            return redirect('post_detail', pk=post.pk)

        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if "publish" in request.POST:
                return redirect('post_publish', pk=post.pk)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form':form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if "cancel_return_to_post" in request.GET:
        return redirect('post_detail', pk=post.pk)
    if "cancel_return_to_list" in request.GET:
        return redirect('post_list')
    if "delete" in request.GET:
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_delete.html', {'post':post})


def post_unpublished_list(request):
    # posts = []
    first_posts = Post.objects.filter(published_date__gt=timezone.now())
    second_posts = Post.objects.filter(published_date__isnull=True)

    posts = sorted(chain(first_posts, second_posts), key=operator.attrgetter('created_date'))

    return render(request, 'blog/post_unpublished_list.html', {'posts':posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect ('post_list')


def comment_new(request, pk):


    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('post_detail', pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            post = Post.objects.get(pk=pk)
            comment.post = post
            comment.created_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_new.html', {'form': form})
