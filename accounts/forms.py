from django import forms
from django.contrib.auth import get_user_model
from core.models import Post
from .models import Contact,Ticket,Reply,CustomUser

User = get_user_model()

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}),label='ایمیل')
    username = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'placeholder':'Enter your username'}),label='نام کاربری')
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}),label='رمز عبور')
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Confirm your password'}),label='تکرار رمز عبور')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلا استفاده شده است.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('پسورد با تکرار آن مطابقت ندارد.')

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','cover_image','slug']

class PasswordResetForm(forms.Form):
    email = forms.EmailField(required=True,label='ایمیل',widget=forms.EmailInput)

class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(required=True,label='رمز جدید',widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=True,label='تکرار رمز جدید',widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError('پسورد و تکرار آن یکی نیست')
        return data

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject','message']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message']

class ProfileImage(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['photo']