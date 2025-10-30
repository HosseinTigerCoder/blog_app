from django.db import models
from django.conf import settings
from django.utils.text import slugify
from accounts.models import CustomUser


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    cover_image = models.ImageField(upload_to='cover image/',blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True,unique=True)
    likes = models.ManyToManyField(CustomUser,related_name='liked_posts',blank=True)

    def count_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    confirm = models.BooleanField(default=False)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies')
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def get_all_replies(self):
        replies = []
        for reply in self.replies.filter(confirm=True):
            replies.append(reply)
            replies.extend(reply.get_all_replies())
        return replies
    
    def __str__(self):
        return f'{self.user} in {self.post}.'
