from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from .forms import CommentForm
from django.core.paginator import Paginator
from django.urls import reverse

# Create your views here.
# @api_view()
def home_page(request):
    posts = Post.objects.order_by('-date_created')[:5]
    return render(request,'index.html',{'posts':posts})
    # queryset = Post.objects.all()
    # serializer = PostSerializer(queryset,many=True)
    # return Response(serializer.data)

def all_posts(request):
    search_query = request.GET.get('search-box','').strip()
    if search_query:
        posts = Post.objects.filter(title__icontains=search_query).order_by('-date_created')
    else:
        posts = Post.objects.all().order_by('-date_created')
        
    # posts = Post.objects.all().order_by('-date_created')

    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not search_query:
        search_query = ''
    return render(request,'posts.html',{'page_obj':page_obj,'search_query':search_query})

@login_required(login_url='login')
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent_id=None,confirm=True).order_by('-date_created')

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
    return render(request, 'post-detail.html', context)

def like_post(request,slug):
    if request.method == 'POST':
        post = get_object_or_404(Post,slug=slug)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('post_detail',slug=slug)