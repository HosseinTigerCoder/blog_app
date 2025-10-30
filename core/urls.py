from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page,name='home'),
    path('post/<slug:slug>',views.post_detail,name='post_detail'),
    path('posts/',views.all_posts,name='posts'),
    path('like/<slug:slug>',views.like_post,name='liked_post')
]