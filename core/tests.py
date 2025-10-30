from django.test import TestCase,Client
from .models import Post
from accounts.models import CustomUser
from django.urls import reverse

# Create your tests here.
class TestViewsCore(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user('admin','admin@gmail.com','1234')
        self.post = Post.objects.create(author=self.user,title='موز',text='علی موز میخورد',slug='moz')
        self.client = Client()

    def test_view_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
    
    def test_post_detail_page(self):
        self.client.login(username='admin@gmail.com', password='1234')
        response = self.client.get(reverse('post_detail',args=[self.post.slug]))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,self.post.title)
    
    def test_post_list_view(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'posts.html')

class PostModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user('admin','admin@gmail.com','1234')
        self.post = Post.objects.create(author=self.user,title='پست تستی',text='محتوای تستی',slug='test')

    def test_post_created(self):
        self.assertEqual(self.post.title,'پست تستی')

    def test_post_str_method(self):
        self.assertEqual(str(self.post),self.post.title)