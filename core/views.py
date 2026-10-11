from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from .forms import CommentForm
from django.core.paginator import Paginator
from django.db.models import Q,F
from django.urls import reverse

# Create your views here.
def home_page(request):
    posts = Post.objects.order_by('-date_created')[:6]
    popular_posts = Post.objects.order_by('-views')[:5]
    return render(request,'blog/index.html',{'posts':posts,'popular_posts':popular_posts})

def all_posts(request):
    search_query = request.GET.get('search-box','').strip()
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query)).order_by('-date_created')
    else:
        posts = Post.objects.all().order_by('-date_created')
        
    # posts = Post.objects.all().order_by('-date_created')

    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not search_query:
        search_query = ''
    return render(request,'blog/posts.html',{'page_obj':page_obj,'search_query':search_query})

@login_required(login_url='login')
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent_id=None,confirm=True).order_by('-date_created')

    session_key = f'viewed_post_{post.pk}'

    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
        request.session[session_key] = True
        post.refresh_from_db(fields=['views'])
    # post.views += 1
    # post.save(update_fields=['views'])

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            # parent_comment = Comment.objects.get(id=parent_id) if parent_id else None
            parent_comment = None
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    parent_comment = None

            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.user = request.user

            if request.user.email == 'admin@gmail.com':
                new_comment.confirm = True  # ادمین تایید کنه خودش فعال میشه

            new_comment.save()
            return redirect('post_detail',slug=slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/post-detail.html', context)

def like_post(request,slug):
    if request.method == 'POST':
        post = get_object_or_404(Post,slug=slug)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('post_detail',slug=slug)