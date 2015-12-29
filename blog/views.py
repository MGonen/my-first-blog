from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.db.models import Q
import operator
from itertools import chain


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    unsorted_comments_queryset = Comment.objects.filter(post=pk).order_by('created_date')
    unsorted_comments = []
    for comment in unsorted_comments_queryset:
        unsorted_comments.append(comment)

    comments = sort_comments(unsorted_comments)

    already_published = True
    if not post.published_date or post.published_date > timezone.now():
        already_published = False

    return render(request, 'blog/post_detail.html', {'post':post, 'already_published':already_published, 'comments':comments })


def sort_comments(unsorted_comments):
    sorted_comments = []

    while unsorted_comments != []:
        print 'while loop iteration'
        original_comment = unsorted_comments[0]
        unsorted_comments, sorted_comments = recursive_sorting(unsorted_comments, sorted_comments, original_comment)

    return sorted_comments

def recursive_sorting(unsorted_comments, sorted_comments, org_comment):
    unsorted_copy = unsorted_comments[:]

    child_comment_found = False
    for comment in unsorted_copy:
        if comment.parent_comment:
            if comment.parent_comment.id == org_comment.id:
                child_comment_found = True
                if org_comment not in sorted_comments:
                    sorted_comments.append(org_comment)
                recursive_sorting(unsorted_comments, sorted_comments, comment)

    if not child_comment_found:
        sorted_comments.append(org_comment)
    unsorted_comments.remove(org_comment)
    return unsorted_comments, sorted_comments





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
    posts = Post.objects.filter(Q(published_date__gt=timezone.now()) | Q(published_date__isnull=True)).order_by('created_date')
    # posts = Post.objects.filter(Q(published_date__gt=timezone.now()) | Q(published_date__isnull=True)).order_by('created_date')


    return render(request, 'blog/post_unpublished_list.html', {'posts':posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect ('post_list')


def comment_new(request, post_pk, comment_pk):
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('post_detail', post_pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            post = Post.objects.get(pk=post_pk)
            comment.post = post
            comment.created_date = timezone.now()
            if comment_pk != '0':
                parent_comment = Comment.objects.get(pk=comment_pk)
                comment.parent_comment = parent_comment
                comment.level = parent_comment.level + 1
            comment.save()
            return redirect('post_detail', pk=post_pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_new.html', {'form': form})


def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('post_detail', pk=post_pk)










