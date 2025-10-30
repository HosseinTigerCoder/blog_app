from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='profile/',null=True,blank=True)
    about = models.CharField(max_length=255,null=True,blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=20)
    text = models.TextField()

class Ticket(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'موضوع تیکت : {self.subject}'

class Reply(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name='replies')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    message = message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)