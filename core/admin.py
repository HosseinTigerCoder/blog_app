from django.contrib import admin
from . import models
from django.utils.html import format_html,urlencode
from django.urls import reverse
from django.db.models import Count
from .forms import PostAdminForm

# Register your models here.
# admin.site.register(models.Post)

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title','author_name','slug','comments_count','count_views']
    list_filter = ['title']
    list_per_page = 10
    prepopulated_fields = {'slug':['title',]}

    def author_name(self,post):
        return post.author
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(comments_count=Count('comments'))
  
    def comments_count(self,post):
        url = (reverse('admin:core_comment_changelist') + '?' + urlencode({'post__id':str(post.id)}))
        return format_html('<a href="{}">{}</a>',url,post.comments_count)

    def count_views(self,post):
        return post.views

    count_views.short_description = 'تعداد بازدید'
    comments_count.short_description = 'تعداد کامنت ها'    
    author_name.short_description = 'نویسنده'

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','text','user','confirm']
    list_editable = ['confirm']
    list_filter = ['post','user','confirm']
    list_per_page = 10
    actions = ['confirm_comments']

    def confirm_comments(self,request,queryset):
        queryset.update(confirm=True)

    confirm_comments.short_description = 'تایید کامنت ها'