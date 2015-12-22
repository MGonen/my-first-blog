from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})


def post_new(request):
    print 'request = ', request
    if request.method == "POST":
        print 'request.POST = ', request.POST

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        print 'request.GET =', request.GET
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form':form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_delete.html', {'post':post})


def post_unpublished_list(request):
    first_posts = Post.objects.filter(published_date__gte=timezone.now())
    second_posts = Post.objects.filter(published_date=None)
    posts = []
    for item in first_posts:
        posts.append(item)
    for item in second_posts:
        posts.append(item)


    return render(request, 'blog/post_unpublished_list.html', {'posts':posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect ('post_list')