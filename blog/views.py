from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
import operator

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    already_published = True
    if not post.published_date or post.published_date > timezone.now():
        already_published = False

    return render(request, 'blog/post_detail.html', {'post':post, 'already_published':already_published})


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
    # first_posts_query_set = Post.objects.filter(published_date__gt=timezone.now()).order_by('created_date')
    # first_posts = []
    # for item in first_posts_query_set:
    #     first_posts.append(item)
    #
    # second_posts_query_set = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    # second_posts = []
    # for item in second_posts_query_set:
    #     second_posts.append(item)
    # posts = []
    #
    # while first_posts != [] and second_posts != []:
    #     if first_posts != []:
    #         if first_posts[0].created_date < second_posts[0].created_date:
    #             posts.append(first_posts[0])
    #             del first_posts[0]
    #         else:
    #             posts.append(second_posts[0])
    #             del second_posts[0]
    #
    # if first_posts == []:
    #     for item in second_posts:
    #         posts.append(item)
    # else:
    #     for item in first_posts:
    #         posts.append(item)

    posts = []
    first_posts = Post.objects.filter(published_date__gt=timezone.now())
    second_posts = Post.objects.filter(published_date__isnull=True)

    for item in first_posts:
        posts.append(item)
    for item in second_posts:
        posts.append(item)

    posts = sorted(posts, key=operator.attrgetter('created_date'))

    return render(request, 'blog/post_unpublished_list.html', {'posts':posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect ('post_list')